import boto3
from rich.console import Console
from rich import print

from ...report.print import (
    print_namespace_table,
    print_service_table,
)
from ...helpers import ApiConfig

console = Console()


def check_default_deny_policy_exists(api_config: ApiConfig):
    offenders = [i.metadata.name for i in api_config.namespaces]

    for policy in api_config.network_policies:
        offenders.remove(policy.metadata.namespace)

    if offenders:
        print_namespace_table(
            offenders,
            "Namespaces that does not have default network deny policies",
        )

    return offenders


def check_vpc_flow_logs(api_config: ApiConfig):
    client = boto3.client("eks", region_name=api_config.region)
    cluster_metadata = client.describe_cluster(name=api_config.cluster)
    vpc_id = cluster_metadata["cluster"]["resourcesVpcConfig"]["vpcId"]
    client = boto3.client("ec2")

    flow_logs = client.describe_flow_logs(
        Filters=[{"Name": "resource-id", "Values": [vpc_id]}]
    )["FlowLogs"]

    query = """
fields @timestamp, @message
| sort @timestamp desc
    """

    if not flow_logs:
        console.print("Enable flow logs for your VPC.", style="red")
        console.print()
        console.print("*" * 100)
        return True


def use_encryption_with_aws_load_balancers(api_config: ApiConfig):
    offenders = []

    for service in api_config.services:
        annotations = service.metadata.annotations
        if annotations and not (
            annotations.get("service.beta.kubernetes.io/aws-load-balancer-ssl-cert") and
            annotations.get("service.beta.kubernetes.io/aws-load-balancer-ssl-ports") == "443"
        ):
            offenders.append(service)
            
    if offenders:
        print_service_table(
            offenders, "Make sure you specify an ssl cert"
        )
    return offenders 