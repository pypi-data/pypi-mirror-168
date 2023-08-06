from typing import List
from unittest.mock import Mock, patch

import pytest
from ray.autoscaler._private.aws.config import DEFAULT_RAY_IAM_ROLE

from anyscale.cloud_resource import (
    verify_aws_cloudformation_stack,
    verify_aws_efs,
    verify_aws_iam_roles,
    verify_aws_s3,
    verify_aws_security_groups,
    verify_aws_subnets,
    verify_aws_vpc,
)
from anyscale.conf import ANYSCALE_IAM_ROLE_NAME
from frontend.cli.anyscale.aws_iam_policies import (
    AMAZON_ECR_READONLY_ACCESS_POLICY_NAME,
    AMAZON_S3_FULL_ACCESS_POLICY_NAME,
    ANYSCALE_IAM_PERMISSIONS_EC2_INITIAL_RUN,
    ANYSCALE_IAM_PERMISSIONS_EC2_STEADY_STATE,
    ANYSCALE_IAM_POLICY_NAME_INITIAL_RUN,
    ANYSCALE_IAM_POLICY_NAME_STEADY_STATE,
)
from frontend.cli.anyscale.client.openapi_client.models.create_cloud_resource import (
    CreateCloudResource,
)


def generate_cloud_resource_mock_aws() -> CreateCloudResource:
    return CreateCloudResource(
        aws_vpc_id="fake_aws_vpc_id",
        aws_subnet_ids=["fake_aws_subnet_id_0"],
        aws_iam_role_arns=["arn:aws:iam::123:role/mock_anyscale_role"],
        aws_security_groups=["fake_aws_security_group_0"],
        aws_s3_id="fake_aws_s3_id",
        aws_efs_id="fake_aws_efs_id",
        aws_cloudformation_stack_id="fake_aws_cloudformation_stack_id",
    )


def generate_cluod_aws_iam_roles() -> List[Mock]:
    anyscale_iam_role = Mock(role_name=ANYSCALE_IAM_ROLE_NAME)
    steady_state_policy = Mock(
        policy_name=ANYSCALE_IAM_POLICY_NAME_STEADY_STATE,
        policy_document=ANYSCALE_IAM_PERMISSIONS_EC2_STEADY_STATE,
    )
    initial_run_policy = Mock(
        policy_name=ANYSCALE_IAM_POLICY_NAME_INITIAL_RUN,
        policy_document=ANYSCALE_IAM_PERMISSIONS_EC2_INITIAL_RUN,
    )
    anyscale_iam_role.policies.all = Mock(
        return_value=[steady_state_policy, initial_run_policy]
    )

    ray_iam_role = Mock(role_name=DEFAULT_RAY_IAM_ROLE)
    ecr_readonly_policy = Mock(policy_name=AMAZON_ECR_READONLY_ACCESS_POLICY_NAME)
    s3_full_access_policy = Mock(policy_name=AMAZON_S3_FULL_ACCESS_POLICY_NAME)
    ray_iam_role.attached_policies.all = Mock(
        return_value=[ecr_readonly_policy, s3_full_access_policy]
    )

    return [anyscale_iam_role, ray_iam_role]


def generate_aws_security_groups() -> List[Mock]:
    ip_permission_443 = {"FromPort": 443}
    ip_permission_22 = {"FromPort": 22}
    ip_permission_2049 = {"FromPort": 2049}
    inbound_ip_permissions = [ip_permission_443, ip_permission_22, ip_permission_2049]
    anyscale_security_group = Mock(ip_permissions=inbound_ip_permissions)
    return anyscale_security_group


@pytest.mark.parametrize(
    "vpc_exists,vpc_cidr_block,expected_result",
    [
        pytest.param(False, "0.0.0.0/0", False),
        pytest.param(True, "0.0.0.0/16", True),
        pytest.param(True, "1.23.45.67/20", False),
    ],
)
def test_verify_aws_vpc(vpc_exists: bool, vpc_cidr_block: str, expected_result: bool):
    cloud_resource_mock = generate_cloud_resource_mock_aws()
    ec2_mock = Mock()
    vpc_mock = Mock(cidr_block=vpc_cidr_block) if vpc_exists else None
    ec2_mock.Vpc = Mock(return_value=vpc_mock)
    with patch("anyscale.cloud_resource.boto3.resource", Mock(return_value=ec2_mock)):
        result = verify_aws_vpc(cloud_resource=cloud_resource_mock, logger=Mock())
        assert result == expected_result


@pytest.mark.parametrize(
    "subnets_exist,subnet_cidr_block,subnet_vpc_matches,expected_result",
    [
        pytest.param(False, "0.0.0.0/0", True, False),
        pytest.param(True, "0.0.0.0/20", True, True),
        pytest.param(True, "0.0.0.0/20", False, False),
        pytest.param(True, "0.1.2.3/21", True, False),
    ],
)
def test_verify_aws_subnets(
    subnets_exist: bool,
    subnet_cidr_block: str,
    subnet_vpc_matches: bool,
    expected_result: bool,
):
    cloud_resource_mock = generate_cloud_resource_mock_aws()
    ec2_mock = Mock()
    subnet_mock = (
        Mock(
            cidr_block=subnet_cidr_block,
            vpc_id=cloud_resource_mock.aws_vpc_id if subnet_vpc_matches else "",
        )
        if subnets_exist
        else None
    )
    ec2_mock.Subnet = Mock(return_value=subnet_mock)
    with patch(
        "anyscale.cloud_resource.boto3.resource", Mock(return_value=ec2_mock)
    ), patch.multiple(
        "anyscale.cloud_resource", verify_aws_iam_roles=Mock(return_value=True)
    ):
        result = verify_aws_subnets(cloud_resource=cloud_resource_mock, logger=Mock())
        assert result == expected_result


def test_verify_aws_iam_roles():
    cloud_resource_mock = generate_cloud_resource_mock_aws()
    iam_roles_mock = generate_cluod_aws_iam_roles()
    with patch(
        "anyscale.cloud_resource._get_roles_from_role_names",
        Mock(return_value=iam_roles_mock),
    ):
        result = verify_aws_iam_roles(
            cloud_resource=cloud_resource_mock, region="fake_region", logger=Mock()
        )
        assert result


def test_verify_aws_security_groups():
    cloud_resource_mock = generate_cloud_resource_mock_aws()
    security_group_mock = generate_aws_security_groups()
    ec2_mock = Mock()
    ec2_mock.SecurityGroup = Mock(return_value=security_group_mock)
    with patch("anyscale.cloud_resource.boto3.resource", Mock(return_value=ec2_mock)):
        result = verify_aws_security_groups(
            cloud_resource=cloud_resource_mock, logger=Mock()
        )
        assert result


@pytest.mark.parametrize(
    "s3_exists,expected_result", [pytest.param(False, False), pytest.param(True, True)]
)
def test_verify_aws_s3(s3_exists: bool, expected_result: bool):
    cloud_resource_mock = generate_cloud_resource_mock_aws()
    s3_mock = Mock()
    s3_bucket_mock = Mock() if s3_exists else None
    s3_mock.Bucket = Mock(return_value=s3_bucket_mock)
    with patch("anyscale.cloud_resource.boto3.resource", Mock(return_value=s3_mock)):
        result = verify_aws_s3(cloud_resource=cloud_resource_mock, logger=Mock())
        assert result == expected_result


@pytest.mark.parametrize(
    "efs_exists,expected_result",
    [pytest.param(False, False), pytest.param(True, True)],
)
def test_verify_aws_efs(efs_exists: bool, expected_result: bool):
    cloud_resource_mock = generate_cloud_resource_mock_aws()
    efs_client_mock = Mock()
    efs_response_mock = {"FileSystems": Mock() if efs_exists else None}
    efs_client_mock.describe_file_systems = Mock(return_value=efs_response_mock)
    with patch(
        "anyscale.cloud_resource.boto3.client", Mock(return_value=efs_client_mock)
    ):
        result = verify_aws_efs(cloud_resource=cloud_resource_mock, logger=Mock())
        assert result == expected_result


@pytest.mark.parametrize(
    "cloudformation_stack_exists,expected_result",
    [pytest.param(False, False), pytest.param(True, True)],
)
def test_verify_aws_cloudformation_stack(
    cloudformation_stack_exists: bool, expected_result: bool
):
    cloud_resource_mock = generate_cloud_resource_mock_aws()
    cloudformation_mock = Mock()
    cloudformation_stack_mock = Mock() if cloudformation_stack_exists else None
    cloudformation_mock.Stack = Mock(return_value=cloudformation_stack_mock)
    with patch(
        "anyscale.cloud_resource.boto3.resource", Mock(return_value=cloudformation_mock)
    ):
        result = verify_aws_cloudformation_stack(
            cloud_resource=cloud_resource_mock, logger=Mock()
        )
        assert result == expected_result
