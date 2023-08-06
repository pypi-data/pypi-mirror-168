"""
Fetches data required and formats output for `anyscale cloud` commands.
"""

import ipaddress
import json
import secrets
from typing import Any, Dict, Optional

import boto3
import botocore
import click
from click import ClickException, INT, prompt
from ray.autoscaler._private.aws.config import DEFAULT_RAY_IAM_ROLE

from anyscale.aws_iam_policies import (
    AMAZON_ECR_READONLY_ACCESS_POLICY_ARN,
    AMAZON_S3_FULL_ACCESS_POLICY_ARN,
    ANYSCALE_IAM_PERMISSIONS_EC2_INITIAL_RUN,
    ANYSCALE_IAM_PERMISSIONS_EC2_STEADY_STATE,
    ANYSCALE_IAM_POLICY_NAME_INITIAL_RUN,
    ANYSCALE_IAM_POLICY_NAME_STEADY_STATE,
    ANYSCALE_SSM_READ_WRITE_ACCESS_POLICY_DOCUMENT,
    ANYSCALE_SSM_READONLY_ACCESS_POLICY_DOCUMENT,
)
from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client.models import Cloud, CloudConfig, WriteCloud
from anyscale.cloud import get_cloud_id_and_name, get_cloud_json_from_id
from anyscale.conf import ANYSCALE_IAM_ROLE_NAME
from anyscale.controllers.base_controller import BaseController
from anyscale.formatters import clouds_formatter
from anyscale.util import (  # pylint:disable=private-import
    _CACHED_GCP_REGIONS,
    _client,
    _get_role,
    _resource,
    _update_external_ids_for_policy,
    confirm,
    get_available_regions,
    launch_gcp_cloud_setup,
)


ROLE_CREATION_RETRIES = 30
ROLE_CREATION_INTERVAL_SECONDS = 1


class CloudController(BaseController):
    def __init__(
        self, log: BlockLogger = BlockLogger(), initialize_auth_api_client: bool = True
    ):
        super().__init__(initialize_auth_api_client=initialize_auth_api_client)
        self.log = log
        self.log.open_block("Output")

    def delete_cloud(
        self,
        cloud_name: Optional[str],
        cloud_id: Optional[str],
        skip_confirmation: bool,
    ) -> bool:
        """
        Deletes a cloud by name or id.
        """

        if not cloud_id and not cloud_name:
            raise ClickException("Must either provide the cloud name or cloud id.")

        cloud_id, cloud_name = get_cloud_id_and_name(
            self.api_client, cloud_id, cloud_name
        )

        confirm(
            f"You'll lose access to existing sessions created with cloud {cloud_id} if you drop it.\nContinue?",
            skip_confirmation,
        )

        cloud = self.api_client.get_cloud_api_v2_clouds_cloud_id_get(
            cloud_id=cloud_id
        ).result
        if cloud.provider.lower() == "aws" and not cloud.is_k8s and not cloud.is_aioa:
            self.delete_aws(cloud.region, cloud.credentials)

        self.api_client.delete_cloud_api_v2_clouds_cloud_id_delete(cloud_id=cloud_id)

        self.log.info(f"Deleted cloud {cloud_name}")

        return True

    def list_clouds(self, cloud_name: Optional[str], cloud_id: Optional[str]) -> str:
        if cloud_id is not None:
            clouds = [
                self.api_client.get_cloud_api_v2_clouds_cloud_id_get(cloud_id).result
            ]
        elif cloud_name is not None:
            clouds = [
                self.api_client.find_cloud_by_name_api_v2_clouds_find_by_name_post(
                    {"name": cloud_name}
                ).result
            ]
        else:
            clouds = self.api_client.list_clouds_api_v2_clouds_get().results
        output = clouds_formatter.format_clouds_output(clouds=clouds, json_format=False)

        return str(output)

    def verify_vpc_peering(
        self,
        yes: bool,
        vpc_peering_ip_range: Optional[str],
        vpc_peering_target_project_id: Optional[str],
        vpc_peering_target_vpc_id: Optional[str],
    ) -> None:
        if (
            vpc_peering_ip_range
            or vpc_peering_target_project_id
            or vpc_peering_target_vpc_id
        ):
            if not vpc_peering_ip_range:
                raise ClickException("Please specify a VPC peering IP range.")
            if not vpc_peering_target_project_id:
                raise ClickException("Please specify a VPC peering target project ID.")
            if not vpc_peering_target_vpc_id:
                raise ClickException("Please specify a VPC peering target VPC ID.")
        else:
            return

        try:
            valid_ip_network = ipaddress.IPv4Network(vpc_peering_ip_range)
        except ValueError:
            raise ClickException(f"{vpc_peering_ip_range} is not a valid IP address.")
        # https://cloud.google.com/vpc/docs/vpc#valid-ranges
        allowed_ip_ranges = [
            ipaddress.IPv4Network("10.0.0.0/8"),
            ipaddress.IPv4Network("172.16.0.0/12"),
            ipaddress.IPv4Network("192.168.0.0/16"),
        ]

        for allowed_ip_range in allowed_ip_ranges:
            if valid_ip_network.subnet_of(allowed_ip_range):
                break
        else:
            raise ClickException(
                f"{vpc_peering_ip_range} is not a allowed private IP address range for GCP. The allowed IP ranges are 10.0.0.0/8, 172.16.0.0/12, and 192.168.0.0/16. For more info, see https://cloud.google.com/vpc/docs/vpc#valid-ranges"
            )

        if (
            valid_ip_network.num_addresses
            < ipaddress.IPv4Network("192.168.0.0/16").num_addresses
        ):
            raise ClickException(
                f"{vpc_peering_ip_range} is not a valid IP range. The minimum size is /16"
            )

        if not yes:
            confirm(
                f"\nYou selected to create a VPC peering connection to VPC {vpc_peering_target_vpc_id} in GCP project {vpc_peering_target_project_id}."
                f"This will create a VPC peering connection from your Anyscale GCP project to the target project ({vpc_peering_target_project_id})."
                "You will need to manually create the peering connection from the target project to your Anyscale GCP project after the anyscale cloud is created.\n"
                "Continue cloud setup?",
                False,
            )

    def setup_cloud(
        self,
        provider: str,
        region: Optional[str],
        name: str,
        yes: bool = False,
        gce: bool = False,
        folder_id: Optional[int] = None,
        vpc_peering_ip_range: Optional[str] = None,
        vpc_peering_target_project_id: Optional[str] = None,
        vpc_peering_target_vpc_id: Optional[str] = None,
    ) -> None:
        """
        Sets up a cloud provider
        """
        if provider == "aws":
            # If the region is blank, change it to the default for AWS.
            if region is None:
                region = "us-west-2"
            regions_available = get_available_regions()
            if region not in regions_available:
                raise ClickException(
                    f"Region '{region}' is not available. Regions available are: "
                    f"{', '.join(map(repr, regions_available))}"
                )
            self.setup_aws(region=region, name=name, yes=yes)
        elif provider == "gcp":
            # If the region is blank, change it to the default for GCP.
            if region is None:
                region = "us-west1"
            # Warn the user about a bad region before the cloud configuration begins.
            # GCP's `list regions` API requires a project, meaning true verification
            # happens in the middle of the flow.
            if region not in _CACHED_GCP_REGIONS and not yes:
                confirm(
                    f"You selected the region: {region}, but it is not in"
                    f"the cached list of GCP regions:\n\n{_CACHED_GCP_REGIONS}.\n"
                    "Continue cloud setup with this region?",
                    False,
                )
            if not yes and not folder_id:
                folder_id = prompt(
                    "Please select the GCP Folder ID where the 'Anyscale' folder will be created.\n"
                    "\tYour GCP account must have permissions to create sub-folders in the specified folder.\n"
                    "\tView your organization's folder layout here: https://console.cloud.google.com/cloud-resource-manager\n"
                    "\tIf not specified, the 'Anyscale' folder will be created directly under the organization.\n"
                    "Folder ID (numerals only)",
                    default="",
                    type=INT,
                    show_default=False,
                )

            self.verify_vpc_peering(
                yes,
                vpc_peering_ip_range,
                vpc_peering_target_project_id,
                vpc_peering_target_vpc_id,
            )
            # TODO: interactive setup process through the CLI?
            launch_gcp_cloud_setup(
                name=name,
                region=region,
                is_k8s=not gce,
                folder_id=folder_id,
                vpc_peering_ip_range=vpc_peering_ip_range,
                vpc_peering_target_project_id=vpc_peering_target_project_id,
                vpc_peering_target_vpc_id=vpc_peering_target_vpc_id,
            )
        else:
            raise ClickException(
                f"Invalid Cloud provider: {provider}. Available providers are [aws, gcp]."
            )

    def delete_aws(self, region: str, role_arn: str) -> None:
        role_name = role_arn.split("/")[-1]

        self.delete_aws_cross_account_role(region, role_name)
        self.log.info(
            f"Delete {DEFAULT_RAY_IAM_ROLE} manually if you are not using Ray OSS."
        )

    def delete_aws_cross_account_role(self, region: str, role_name: str) -> None:
        should_delete_iam_role = False
        if role_name == ANYSCALE_IAM_ROLE_NAME:
            should_delete_iam_role = click.confirm(
                f"\nYou are about to delete IAM role {ANYSCALE_IAM_ROLE_NAME}.\n"
                "Please make sure no clouds in this account is using this role.\n",
            )
        elif ANYSCALE_IAM_ROLE_NAME in role_name:
            should_delete_iam_role = True

        if should_delete_iam_role:
            self.log.info("Deleting AWS cross account roles ...")
            try:
                role = _get_role(role_name=role_name, region=region)
                if role:
                    for policy in role.policies.all():
                        policy.delete()
                    role.delete()
            except botocore.exceptions.ClientError:
                self.log.info(
                    f"Failed to delete IAM role during cloud deletion: {role_name}"
                )
                return
            self.log.info("AWS cross account roles deletion complete.")

    def setup_aws(self, region: str, name: str, yes: bool = False) -> None:

        confirm(
            "\nYou are about to give Anyscale access to EC2 permissions necessary to manage clusters.\n"
            "A separate AWS role is created for your clusters to run with \nand will be granted readonly access to ECR & S3 Full Access in your AWS account.\n\n"
            "Continue?",
            yes,
        )

        self.setup_aws_cross_account_role(region, name)
        self.setup_aws_ray_role(region, DEFAULT_RAY_IAM_ROLE)

        self.log.info("AWS credentials setup complete.")
        self.log.info(
            "You can revoke the access at any time by deleting anyscale IAM user/role in your account."
        )
        self.log.info(
            "Head over to the web UI to create new sessions in your AWS account."
        )

    def setup_aws_cross_account_role(self, region: str, name: str) -> None:
        response = (
            self.api_client.get_anyscale_aws_account_api_v2_clouds_anyscale_aws_account_get()
        )

        anyscale_aws_account = response.result.anyscale_aws_account
        anyscale_aws_iam_role_policy: Dict[str, Any] = {
            "Version": "2012-10-17",
            "Statement": {
                "Sid": "AnyscaleControlPlaneAssumeRole",
                "Effect": "Allow",
                "Principal": {"AWS": anyscale_aws_account},
                "Action": "sts:AssumeRole",
            },
        }

        for _ in range(5):
            role_name = "{}-{}".format(ANYSCALE_IAM_ROLE_NAME, secrets.token_hex(4))

            role = _get_role(role_name, region)
            if role is None:
                break
        else:
            raise RuntimeError(
                "We weren't able to connect your account with the Anyscale because we weren't able to find an available IAM Role name in your account. Please reach out to support or your SA for assistance."
            )

        iam = _resource("iam", region)
        iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(anyscale_aws_iam_role_policy),
        )
        role = _get_role(role_name, region)

        assert role is not None, "Failed to create IAM role."

        role.Policy(name=ANYSCALE_IAM_POLICY_NAME_STEADY_STATE).put(
            PolicyDocument=json.dumps(ANYSCALE_IAM_PERMISSIONS_EC2_STEADY_STATE)
        )

        role.Policy(name=ANYSCALE_IAM_POLICY_NAME_INITIAL_RUN).put(
            PolicyDocument=json.dumps(ANYSCALE_IAM_PERMISSIONS_EC2_INITIAL_RUN)
        )

        self.log.info(f"Using IAM role {role.arn}")
        try:

            created_cloud = self.api_client.create_cloud_api_v2_clouds_post(
                write_cloud=WriteCloud(
                    provider="AWS", region=region, credentials=role.arn, name=name,
                )
            )
        except ClickException:
            self.log.info("Create failed, cleaning up IAM role: {}".format(role_name))
            try:
                for policy in role.policies.all():
                    policy.delete()
                role.delete()
            except botocore.exceptions.ClientError:
                self.log.error(
                    "Failed to clean up IAM role after a failed cloud creation: {}".format(
                        role_name
                    )
                )
            raise
        cloud_id = created_cloud.result.id

        iam_client = _client("iam", region)
        iam_client.update_role(
            RoleName=role.name,
            Description="Anyscale access role for cloud {} in region {}".format(
                cloud_id, created_cloud.result.region
            ),
        )

        # NOTE: We update this _after_ cloud creation because this External ID MUST
        # come from Anyscale, not the customer. We are using the `cloud_id` as it is unique per cloud.
        # https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html
        new_policy = _update_external_ids_for_policy(
            role.assume_role_policy_document, cloud_id
        )

        role.AssumeRolePolicy().update(PolicyDocument=json.dumps(new_policy))

    def setup_aws_ray_role(self, region: str, role_name: str) -> None:
        iam = boto3.resource("iam", region_name=region)

        role = _get_role(role_name, region)
        if role is None:
            iam.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(
                    {
                        "Version": "2012-10-17",
                        "Statement": {
                            "Effect": "Allow",
                            "Principal": {"Service": ["ec2.amazonaws.com"]},
                            "Action": "sts:AssumeRole",
                        },
                    }
                ),
            )

            role = _get_role(role_name, region)

        role.attach_policy(PolicyArn=AMAZON_ECR_READONLY_ACCESS_POLICY_ARN)
        # Modified permissions from Ray (no EC2FullAccess)
        role.attach_policy(PolicyArn=AMAZON_S3_FULL_ACCESS_POLICY_ARN)

        for profile in role.instance_profiles.all():
            if profile.name == role_name:
                return
        profile = iam.create_instance_profile(InstanceProfileName=role_name)
        profile.add_role(RoleName=role_name)

    def update_cloud_config(
        self,
        cloud_name: Optional[str],
        cloud_id: Optional[str],
        max_stopped_instances: int,
    ) -> None:
        """Updates a cloud's configuration by name or id.

        Currently the only supported option is "max_stopped_instances."
        """

        if not cloud_id and not cloud_name:
            raise ClickException("Must either provide the cloud name or cloud id.")

        cloud_id, cloud_name = get_cloud_id_and_name(
            self.api_client, cloud_id, cloud_name
        )

        self.api_client.update_cloud_config_api_v2_clouds_cloud_id_config_put(
            cloud_id=cloud_id,
            cloud_config=CloudConfig(max_stopped_instances=max_stopped_instances),
        )

        self.log.info(f"Updated config for cloud '{cloud_name}' to:")
        self.log.info(self.get_cloud_config(cloud_name=None, cloud_id=cloud_id))

    def get_cloud_config(
        self, cloud_name: Optional[str] = None, cloud_id: Optional[str] = None,
    ) -> str:
        """Get a cloud's current JSON configuration."""

        if not cloud_id and not cloud_name:
            raise ClickException("Must either provide the cloud name or cloud id.")

        cloud_id, cloud_name = get_cloud_id_and_name(
            self.api_client, cloud_id, cloud_name
        )

        return str(get_cloud_json_from_id(cloud_id, self.api_client)["config"])

    def set_default_cloud(
        self, cloud_name: Optional[str], cloud_id: Optional[str],
    ) -> None:
        """
        Sets default cloud for caller's organization. This operation can only be performed
        by organization admins, and the default cloud must have organization level
        permissions.
        """

        if not cloud_id and not cloud_name:
            raise ClickException("Must either provide the cloud name or cloud id.")

        cloud_id, cloud_name = get_cloud_id_and_name(
            self.api_client, cloud_id, cloud_name
        )

        self.api_client.update_default_cloud_api_v2_organizations_update_default_cloud_post(
            cloud_id=cloud_id
        )

        self.log.info(f"Updated default cloud to {cloud_name}")

    def experimental_setup_secrets(
        self,
        cloud_name: Optional[str],
        cloud_id: Optional[str],
        write_permissions: bool,
        yes: bool,
    ):
        """
        Given a cloud name, look up its provider and give it permissions to read secrets
        """
        feature_flag_on = self.api_client.check_is_feature_flag_on_api_v2_userinfo_check_is_feature_flag_on_get(
            "wandb-integration-prototype"
        ).result.is_on
        if not feature_flag_on:
            raise ClickException(
                "Secrets can only be set up if the feature flag is enabled. "
                "Please contact Anyscale support to enable the flag."
            )

        cloud_id, cloud_name = get_cloud_id_and_name(
            self.api_client, cloud_id, cloud_name
        )
        cloud = self.api_client.get_cloud_api_v2_clouds_cloud_id_get(cloud_id).result

        self.log.info(
            f"Setting up secrets policy for {cloud.provider} cloud {cloud.name}"
        )

        if cloud.provider == "AWS":
            return self._experimental_grant_secrets_access_aws(
                cloud, write_permissions, yes
            )

        if cloud.provider == "GCP":
            return self._experimental_grant_secrets_access_gcp(
                cloud, write_permissions, yes
            )

        raise ClickException(f"Cloud secrets not supported for {cloud_name}")

    def _experimental_grant_secrets_access_aws(
        self, cloud: Cloud, write_permissions: bool, yes: bool
    ) -> None:
        """Creates IAM policy for SSM readonly access and attaches it to the given role
        Args:
            cloud (Cloud): Cloud object which needs modification
            write_permissions (bool): Whether to add write permissions for Secrets Manager
                to policy
        """

        # Ensure they are in the correct AWS account, by checking account used
        # for Security Token Service
        STS = "sts"
        current_account = boto3.client(
            STS, region_name=cloud.region
        ).get_caller_identity()["Account"]
        # Cloud credentials of format arn:aws:iam::{cloud_account}:role/{cloud_role}
        # Split credentials to get cloud account.
        cloud_account = cloud.credentials.split(":")[4]

        if current_account != cloud_account:
            raise ClickException(
                f"The cloud you specified uses AWS account {cloud_account}, "
                f"but you are currently logged into {current_account}."
            )

        from ray.autoscaler._private.aws.config import DEFAULT_RAY_IAM_ROLE

        if yes:
            role_name = DEFAULT_RAY_IAM_ROLE
        else:
            role_name = prompt(
                "Which AWS role do you want to grant readonly SSM access to?",
                default=DEFAULT_RAY_IAM_ROLE,
                show_default=True,
            )

        role = _get_role(role_name, cloud.region)
        assert (
            role is not None
        ), f"Failed to find IAM role {role_name} in Cloud {cloud.name}! Have you run 'cloud setup'?"

        policy_name = (
            f"anyscale-secrets-read-write-{cloud.id}"
            if write_permissions
            else f"anyscale-secrets-readonly-{cloud.id}"
        )
        policy_document = (
            ANYSCALE_SSM_READ_WRITE_ACCESS_POLICY_DOCUMENT
            if write_permissions
            else ANYSCALE_SSM_READONLY_ACCESS_POLICY_DOCUMENT
        )

        role.Policy(name=policy_name).put(PolicyDocument=json.dumps(policy_document),)
        self.log.info(
            f"Successfully added/updated inline policy {policy_name} on role {role_name}."
        )
        if role_name == DEFAULT_RAY_IAM_ROLE:
            self.log.info(
                f"Note: {role_name} is the default role used for all Anyscale clouds in "
                f"this AWS account, so policy {policy_name} will be used by all clouds "
                "that use this role. We are planning to create a new default role for each "
                "Anyscale cloud in the future."
            )

    def _experimental_grant_secrets_access_gcp(
        self, cloud: Cloud, write_permissions: bool, yes: bool
    ) -> None:
        import google.auth
        import googleapiclient.discovery
        from oauth2client.client import GoogleCredentials

        credentials = GoogleCredentials.get_application_default()
        projects_client = googleapiclient.discovery.build(
            "cloudresourcemanager", "v3", credentials=credentials
        ).projects()

        gcloud_credentials_project_name = google.auth.default()[1]
        anyscale_cloud_project_name = json.loads(cloud.credentials)["project_id"]
        project_name = gcloud_credentials_project_name or anyscale_cloud_project_name
        if not yes:
            if gcloud_credentials_project_name == anyscale_cloud_project_name:
                prompt_str = (
                    "Your current GCloud credentials and the GCP Project associated "
                    f"with Anyscale Cloud {cloud.name} are for {gcloud_credentials_project_name}"
                )
            else:
                prompt_str = (
                    "Your current GCloud credentials "
                    + (
                        f"are for project {gcloud_credentials_project_name}."
                        if gcloud_credentials_project_name
                        else "do not contain a project."
                    )
                    + f"\nThe GCP Project associated with Anyscale Cloud {cloud.name} is {anyscale_cloud_project_name}."
                )
            project_name = prompt(
                (f"{prompt_str}\nWhich project are you using to store secrets?"),
                default=project_name,
            )

        current_policy = projects_client.getIamPolicy(
            resource=f"projects/{project_name}"
        ).execute()

        svc_account = "{}@{}".format(
            cloud.id.replace("_", "-").lower(),
            json.loads(cloud.credentials)["service_account_email"].split("@")[1],
        )

        if not yes:
            svc_account = prompt(
                "Which service account do you want to grant Secrets Manager access to?\n"
                "This defaults to the cloud-specific service account for this cloud",
                default=svc_account,
            )

        if write_permissions:
            current_policy["bindings"].extend(
                [
                    # Granting secretmanager.admin permissions to instance because it is
                    # the only role which supports creating a secret.
                    {
                        "role": "roles/secretmanager.admin",
                        "members": f"serviceAccount:{svc_account}",
                    },
                ]
            )
        else:
            current_policy["bindings"].extend(
                [
                    {
                        "role": "roles/secretmanager.viewer",
                        "members": f"serviceAccount:{svc_account}",
                    },
                    {
                        "role": "roles/secretmanager.secretAccessor",
                        "members": f"serviceAccount:{svc_account}",
                    },
                ]
            )

        projects_client.setIamPolicy(
            resource=f"projects/{project_name}", body={"policy": current_policy}
        ).execute()

        self.log.info(
            f"Successfully updated the IAM policy for projects/{project_name}."
        )

        serviceusage_resource = googleapiclient.discovery.build(
            "serviceusage", "v1", credentials=credentials
        )
        api_state = (
            serviceusage_resource.services()
            .get(name=f"projects/{project_name}/services/secretmanager.googleapis.com")
            .execute()
        )
        if api_state["state"] != "ENABLED":
            if not yes:
                if not click.confirm(
                    f"The project projects/{project_name} doesn't have the Secret Manager "
                    "API enabled. Do you want to enable it?"
                ):
                    return
            (
                serviceusage_resource.services()
                .enable(
                    name=f"projects/{project_name}/services/secretmanager.googleapis.com"
                )
                .execute()
            )
            self.log.info(
                f"Enabled Secret Manager API for projects/{project_name}. This operation "
                "may take a few minutes for the API to be ready."
            )
