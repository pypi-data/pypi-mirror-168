import difflib
import pprint
from typing import Any, Dict, List

import boto3
from click import ClickException
from ray.autoscaler._private.aws.config import DEFAULT_RAY_IAM_ROLE

from anyscale.aws_iam_policies import (
    AMAZON_ECR_READONLY_ACCESS_POLICY_NAME,
    AMAZON_S3_FULL_ACCESS_POLICY_NAME,
    ANYSCALE_IAM_PERMISSIONS_EC2_INITIAL_RUN,
    ANYSCALE_IAM_PERMISSIONS_EC2_STEADY_STATE,
    ANYSCALE_IAM_POLICY_NAME_INITIAL_RUN,
    ANYSCALE_IAM_POLICY_NAME_STEADY_STATE,
)
from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client.models.create_cloud_resource import (
    CreateCloudResource,
)
from anyscale.conf import ANYSCALE_IAM_ROLE_NAME
from anyscale.util import _get_role  # pylint:disable=private-import


AWS_VPC_CIDR_BLOCK_MASK_MAX = 16
AWS_SUBNET_CIDR_BLOCK_MASK_MAX = 20


def compare_dicts_diff(d1: Dict[Any, Any], d2: Dict[Any, Any]) -> str:
    """Returns a string representation of the difference of the two dictionaries.
    Example:

    Input:
    print(compare_dicts_diff({"a": {"c": 1}, "b": 2}, {"a": {"c": 2}, "d": 3}))

    Output:
    - {'a': {'c': 1}, 'b': 2}
    ?             ^    ^   ^

    + {'a': {'c': 2}, 'd': 3}
    ?             ^    ^   ^
    """

    return "\n" + "\n".join(
        difflib.ndiff(pprint.pformat(d1).splitlines(), pprint.pformat(d2).splitlines())
    )


def verify_aws_vpc(cloud_resource: CreateCloudResource, logger: BlockLogger) -> bool:
    logger.info("Verifying VPC ...")
    if not cloud_resource.aws_vpc_id:
        logger.error("Missing VPC id.")
        return False

    ec2 = boto3.resource("ec2")
    vpc = ec2.Vpc(cloud_resource.aws_vpc_id)
    if not vpc:
        logger.error(f"VPC with id {cloud_resource.aws_vpc_id} does not exist.")
        return False

    cidr_block = vpc.cidr_block
    if int(cidr_block.split("/")[-1]) > AWS_VPC_CIDR_BLOCK_MASK_MAX:
        logger.error(
            f"The cidr block range is too small for vpc with id {cloud_resource.aws_vpc_id}."
        )
        return False

    logger.info(f"VPC {cloud_resource.aws_vpc_id} verification succeeded.")
    return True


def verify_aws_subnets(
    cloud_resource: CreateCloudResource, logger: BlockLogger
) -> bool:
    logger.info("Verifying subnets ...")
    if not cloud_resource.aws_subnet_ids:
        logger.error("Missing subnet IDs.")
        return False

    ec2 = boto3.resource("ec2")
    for aws_subnet_id in cloud_resource.aws_subnet_ids:
        subnet = ec2.Subnet(aws_subnet_id)
        if not subnet:
            logger.error(f"Subnet with id {aws_subnet_id} does not exist.")
            return False

        cidr_block = subnet.cidr_block
        if int(cidr_block.split("/")[-1]) > AWS_SUBNET_CIDR_BLOCK_MASK_MAX:
            logger.error(
                f"The cidr block range is too small for subnet with id {aws_subnet_id}."
            )
            return False

        if cloud_resource.aws_vpc_id and subnet.vpc_id != cloud_resource.aws_vpc_id:
            logger.error(
                f"The subnet {aws_subnet_id} is not in a vpc of this cloud. The vpc of this subnet is {subnet.vpc_id} and the vpc of this cloud is {cloud_resource.aws_vpc_id}."
            )
            return False

    logger.info(f"Subnets {cloud_resource.aws_subnet_ids} verification succeeded.")
    return True


def get_role_name_from_role_arn(role_arn: str) -> str:
    try:
        return role_arn.split("/")[1]
    except Exception:
        raise ClickException(f"Invalid role arn provided. {role_arn}")


def _get_roles_from_role_names(names: List[str], region: str) -> List[Any]:
    return [
        _get_role(role_name=iam_role_name, region=region) for iam_role_name in names
    ]


def verify_aws_iam_roles(
    cloud_resource: CreateCloudResource, region: str, logger: BlockLogger
) -> bool:
    logger.info("Verifying IAM roles ...")
    if not cloud_resource.aws_iam_role_arns:
        logger.error("Missing IAM role arns.")
        return False

    role_names = [
        get_role_name_from_role_arn(arn) for arn in cloud_resource.aws_iam_role_arns
    ]

    roles = _get_roles_from_role_names(names=role_names, region=region)
    if not any((ANYSCALE_IAM_ROLE_NAME in role.role_name for role in roles)):
        logger.error(
            "IAM roles of this cloud resource do not contain anyscale iam role."
        )
        return False
    if not any((DEFAULT_RAY_IAM_ROLE in role.role_name for role in roles)):
        logger.error("IAM roles of this cloud resource do not contain ray iam role.")
        return False

    for role in roles:
        if not role:
            logger.error(f"IAM role with arn {role.arn} does not exist.")
            return False

        if ANYSCALE_IAM_ROLE_NAME in role.role_name:
            for policy in role.policies.all():
                if policy.policy_name == ANYSCALE_IAM_POLICY_NAME_STEADY_STATE:
                    if (
                        policy.policy_document
                        != ANYSCALE_IAM_PERMISSIONS_EC2_STEADY_STATE
                    ):
                        logger.error(
                            f"IAM role {role.arn} policy verification failed for policy {ANYSCALE_IAM_POLICY_NAME_STEADY_STATE}."
                        )
                        logger.error(
                            compare_dicts_diff(
                                policy.policy_document,
                                ANYSCALE_IAM_PERMISSIONS_EC2_STEADY_STATE,
                            )
                        )
                        return False
                elif policy.policy_name == ANYSCALE_IAM_POLICY_NAME_INITIAL_RUN:
                    if (
                        policy.policy_document
                        != ANYSCALE_IAM_PERMISSIONS_EC2_INITIAL_RUN
                    ):
                        logger.error(
                            f"IAM role {role.arn} policy verification failed for policy {ANYSCALE_IAM_POLICY_NAME_INITIAL_RUN}."
                        )
                        logger.error(
                            compare_dicts_diff(
                                policy.policy_document,
                                ANYSCALE_IAM_PERMISSIONS_EC2_INITIAL_RUN,
                            )
                        )
                        return False
                else:
                    logger.info(
                        f"Unknown policy {policy.policy_name} for IAM role {role.arn}. Skipping policies verification."
                    )
        elif DEFAULT_RAY_IAM_ROLE in role.role_name:
            policy_names = [
                policy.policy_name for policy in role.attached_policies.all()
            ]
            if AMAZON_ECR_READONLY_ACCESS_POLICY_NAME not in policy_names:
                logger.error(
                    f"Ray role {role.arn} must contain policy {AMAZON_ECR_READONLY_ACCESS_POLICY_NAME}."
                )
                return False
            if AMAZON_S3_FULL_ACCESS_POLICY_NAME not in policy_names:
                logger.error(
                    f"Ray role {role.arn} must contain policy {AMAZON_S3_FULL_ACCESS_POLICY_NAME}."
                )
                return False
        else:
            logger.info(f"Unknown role {role.arn}. Skipping policies verification.")

    logger.info(f"IAM roles {cloud_resource.aws_iam_role_arns} verification succeeded.")
    return True


def verify_aws_security_groups(
    cloud_resource: CreateCloudResource, logger: BlockLogger
) -> bool:
    logger.info("Verifying security groups ...")
    if not cloud_resource.aws_security_groups:
        logger.error("Missing security group IDs.")
        return False

    ec2 = boto3.resource("ec2")
    # Now we only have one security group defining inbound rules.
    anyscale_security_group_arn = cloud_resource.aws_security_groups[0]
    anyscale_security_group = ec2.SecurityGroup(anyscale_security_group_arn)
    if not anyscale_security_group:
        logger.error(
            f"Security group with id {anyscale_security_group_arn} does not exist."
        )
        return False
    inbound_ip_permissions = anyscale_security_group.ip_permissions
    # 443 is for HTTPS ingress
    # 22 is for SSH
    # 2049 is for EFS
    expected_open_ports = [443, 22, 2049]

    for port in expected_open_ports:
        if not any(
            (
                ip_permission["FromPort"] == port
                for ip_permission in inbound_ip_permissions
            )
        ):
            logger.error(
                f"Security group with id {anyscale_security_group_arn} does not contain inbound permission for port {port}."
            )
            return False

    if len(inbound_ip_permissions) > len(expected_open_ports):
        logger.error(
            f"Security group with id {anyscale_security_group_arn} has too many inbound ip permissions. We are only expecting {expected_open_ports} to be open."
        )
        return False

    logger.info(
        f"Security group {cloud_resource.aws_security_groups} verification succeeded."
    )
    return True


def verify_aws_s3(cloud_resource: CreateCloudResource, logger: BlockLogger) -> bool:
    logger.info("Verifying S3 ...")
    if not cloud_resource.aws_s3_id:
        logger.error("Missing S3 ID.")
        return False

    s3 = boto3.resource("s3")
    bucket_name = cloud_resource.aws_s3_id.split(":")[-1]
    s3_bucket = s3.Bucket(bucket_name)
    if not s3_bucket:
        logger.error(f"S3 object with id {cloud_resource.aws_s3_id} does not exist.")
        return False

    logger.info(f"S3 {cloud_resource.aws_s3_id} verification succeeded.")
    return True


def verify_aws_efs(cloud_resource: CreateCloudResource, logger: BlockLogger) -> bool:
    logger.info("Verifying EFS ...")
    if not cloud_resource.aws_efs_id:
        logger.error("Missing EFS ID.")
        return False

    client = boto3.client("efs")
    response = client.describe_file_systems(FileSystemId=cloud_resource.aws_efs_id)
    if not response["FileSystems"]:
        logger.error(f"EFS with id {cloud_resource.aws_efs_id} does not exist.")
        return False

    logger.info(f"S3 {cloud_resource.aws_efs_id} verification succeeded.")
    return True


def verify_aws_cloudformation_stack(
    cloud_resource: CreateCloudResource, logger: BlockLogger
) -> bool:
    logger.info("Verifying CloudFormation stack ...")
    if not cloud_resource.aws_cloudformation_stack_id:
        logger.error("Missing CloudFormation stack id.")
        return False

    cloudformation = boto3.resource("cloudformation")
    stack = cloudformation.Stack(cloud_resource.aws_cloudformation_stack_id)
    if not stack:
        logger.error(
            f"CloudFormation stack with id {cloud_resource.aws_cloudformation_stack_id} does not exist."
        )
        return False

    logger.info(
        f"CloudFormation stack {cloud_resource.aws_cloudformation_stack_id} verification succeeded."
    )
    return True
