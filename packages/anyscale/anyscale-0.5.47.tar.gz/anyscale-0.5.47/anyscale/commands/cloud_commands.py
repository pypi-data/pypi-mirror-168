from typing import Optional

import click

from anyscale.commands.util import OptionPromptNull
from anyscale.controllers.cloud_controller import CloudController


@click.group(
    "cloud",
    short_help="Configure cloud provider authentication for Anyscale.",
    help="""Configure cloud provider authentication and setup
to allow Anyscale to launch instances in your account.""",
)
def cloud_cli() -> None:
    pass


@cloud_cli.command(name="delete", help="Delete a cloud.")
@click.argument("cloud-name", required=False)
@click.option("--name", "-n", help="Delete cloud by name.", type=str)
@click.option(
    "--cloud-id",
    "--id",
    help="Cloud id to delete. Alternative to cloud name.",
    required=False,
)
@click.option(
    "--yes", "-y", is_flag=True, default=False, help="Don't ask for confirmation."
)
def cloud_delete(
    cloud_name: Optional[str], name: Optional[str], cloud_id: Optional[str], yes: bool
) -> None:
    if cloud_name and name and cloud_name != name:
        raise click.ClickException(
            "The positional argument CLOUD_NAME and the keyword argument --name "
            "were both provided. Please only provide one of these two arguments."
        )
    CloudController().delete_cloud(
        cloud_name=cloud_name or name, cloud_id=cloud_id, skip_confirmation=yes
    )


@cloud_cli.command(
    name="set-default",
    help=(
        "Sets default cloud for your organization. This operation can only be performed "
        "by organization admins, and the default cloud must have organization level "
        "permissions."
    ),
)
@click.argument("cloud-name", required=False)
@click.option("--name", "-n", help="Set cloud as default by name.", type=str)
@click.option(
    "--cloud-id",
    "--id",
    help="Cloud id to set as default. Alternative to cloud name.",
    required=False,
)
def cloud_set_default(
    cloud_name: Optional[str], name: Optional[str], cloud_id: Optional[str]
) -> None:
    if cloud_name and name and cloud_name != name:
        raise click.ClickException(
            "The positional argument CLOUD_NAME and the keyword argument --name "
            "were both provided. Please only provide one of these two arguments."
        )
    CloudController().set_default_cloud(
        cloud_name=cloud_name or name, cloud_id=cloud_id
    )


@cloud_cli.command(name="setup", help="Set up a cloud provider.")
@click.option(
    "--provider",
    help="The cloud provider type.",
    required=True,
    prompt="Provider",
    type=click.Choice(["aws", "gcp"], case_sensitive=False),
)
@click.option(
    "--region",
    cls=OptionPromptNull,
    help="Region to set up the credentials in.",
    required=True,
    prompt="Region",
    default_option="provider",
    default=lambda p: "us-west-2" if p == "aws" else "us-west1",
    show_default=True,
)
@click.option("--name", "-n", help="Name of the cloud.", required=True, prompt="Name")
@click.option(
    "--yes", "-y", is_flag=True, default=False, help="Don't ask for confirmation."
)
@click.option(
    "--gce",
    is_flag=True,
    default=False,
    hidden=True,
    help="GCE is the VM stack on GCP.",
)
@click.option(
    "--gcp-folder-id",
    help="Folder ID where the 'Anyscale'  folder will be created.",
    required=False,
    type=int,
)
@click.option(
    "--vpc-peering-ip-range", help="IP range for VPC peering.", required=False
)
@click.option(
    "--vpc-peering-target-project-id",
    help="Project ID of the target VPC.",
    required=False,
)
@click.option(
    "--vpc-peering-target-vpc-id", help="VPC ID of the target VPC.", required=False
)
def setup_cloud(
    provider: str,
    region: str,
    name: str,
    yes: bool,
    gce: bool,
    gcp_folder_id: Optional[int],
    vpc_peering_ip_range: Optional[str],
    vpc_peering_target_project_id: Optional[str],
    vpc_peering_target_vpc_id: Optional[str],
) -> None:
    CloudController().setup_cloud(
        provider=provider,
        region=region,
        name=name,
        yes=yes,
        gce=gce,
        folder_id=gcp_folder_id,
        vpc_peering_ip_range=vpc_peering_ip_range,
        vpc_peering_target_project_id=vpc_peering_target_project_id,
        vpc_peering_target_vpc_id=vpc_peering_target_vpc_id,
    )


@cloud_cli.command(
    name="list", help=("List information about clouds in your Anyscale organization."),
)
@click.option(
    "--name",
    "-n",
    required=False,
    default=None,
    help="Name of cloud to get information about.",
)
@click.option(
    "--cloud-id",
    "--id",
    required=False,
    default=None,
    help=("Id of cloud to get information about."),
)
def list_cloud(name: Optional[str], cloud_id: Optional[str],) -> None:
    print(CloudController().list_clouds(cloud_name=name, cloud_id=cloud_id,))


@cloud_cli.group("config", help="Manage the configuration for a cloud.")
def cloud_config_group() -> None:
    pass


@cloud_config_group.command("update", help="Update the configuration for a cloud.")
@click.argument("cloud-name", required=False)
@click.option(
    "--cloud-id",
    "--id",
    help="Cloud id to update. Alternative to cloud name.",
    required=False,
)
@click.option("--name", "-n", help="Update configuration of cloud by name.", type=str)
@click.option(
    "--max-stopped-instances",
    help="Maximum number of stopped instances permitted in the shared instance pool.",
    required=True,
)
def cloud_config_update(
    cloud_name: Optional[str],
    name: Optional[str],
    cloud_id: Optional[str],
    max_stopped_instances: int,
) -> None:
    if cloud_name and name and cloud_name != name:
        raise click.ClickException(
            "The positional argument CLOUD_NAME and the keyword argument --name "
            "were both provided. Please only provide one of these two arguments."
        )
    CloudController().update_cloud_config(
        cloud_name=cloud_name or name,
        cloud_id=cloud_id,
        max_stopped_instances=max_stopped_instances,
    )


@cloud_config_group.command("get", help="Get the current configuration for a cloud.")
@click.argument("cloud-name", required=False)
@click.option("--name", "-n", help="Update configuration of cloud by name.", type=str)
@click.option(
    "--cloud-id",
    "--id",
    help="Cloud id to get details about. Alternative to cloud name.",
    required=False,
)
def cloud_config_get(
    cloud_name: Optional[str], name: Optional[str], cloud_id: Optional[str]
) -> None:
    if cloud_name and name and cloud_name != name:
        raise click.ClickException(
            "The positional argument CLOUD_NAME and the keyword argument --name "
            "were both provided. Please only provide one of these two arguments."
        )
    print(
        CloudController().get_cloud_config(
            cloud_name=cloud_name or name, cloud_id=cloud_id,
        )
    )


@cloud_cli.command(
    name="secrets",
    help="Allow clusters started in this cloud to access secrets manager.",
    hidden=True,
)
@click.argument("cloud-name", required=False)
@click.option(
    "--name",
    "-n",
    help="Allow clusters started in this cloud (identified by cloud name) to access secrets manager.",
    type=str,
)
@click.option(
    "--cloud-id",
    "--id",
    help="Allow clusters started in this cloud (identified by cloud id) to access secrets manager.",
    required=False,
)
@click.option(
    "--yes", "-y", is_flag=True, default=False, help="Don't ask for confirmation."
)
@click.option(
    "--write-permissions",
    is_flag=True,
    default=False,
    help="Allow clusters starting in this cloud to write to secrets manager as well.",
)
def cloud_secrets(
    cloud_name: Optional[str],
    name: Optional[str],
    cloud_id: Optional[str],
    write_permissions: bool,
    yes: bool,
) -> None:
    if cloud_name and name and cloud_name != name:
        raise click.ClickException(
            "The positional argument CLOUD_NAME and the keyword argument --name "
            "were both provided. Please only provide one of these two arguments."
        )
    CloudController().experimental_setup_secrets(
        cloud_name=cloud_name or name,
        cloud_id=cloud_id,
        write_permissions=write_permissions,
        yes=yes,
    )
