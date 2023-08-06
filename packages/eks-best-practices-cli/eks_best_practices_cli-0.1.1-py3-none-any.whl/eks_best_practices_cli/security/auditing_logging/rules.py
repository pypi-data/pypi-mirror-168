import boto3
from rich.console import Console
from rich import print

from ...helpers import ApiConfig, generate_cloudwatch_query


console = Console()


def check_logs_are_enabled(api_config: ApiConfig):
    client = boto3.client("eks", region_name=api_config.region)
    cluster_metadata = client.describe_cluster(name=api_config.cluster)
    logs = cluster_metadata["cluster"]["logging"]["clusterLogging"][0][
        "enabled"
    ]
    if not logs:
        console.print("Enable control plane logs for auditing", style="red")
        console.print()
        console.print("*" * 100)


def print_aws_auth_config_map_updates(api_config: ApiConfig):
    query = """
fields @timestamp, @message
| filter @logStream like "kube-apiserver-audit"
| filter verb in ["update", "patch"]
| filter objectRef.resource = "configmaps" and objectRef.name = "aws-auth" and objectRef.namespace = "kube-system"
| sort @timestamp desc
    """

    url = generate_cloudwatch_query(
        api_config.region, query, [f"/aws/eks/{api_config.cluster}/cluster"]
    )

    console.print("Check updates to the aws-auth ConfigMap", style="red")
    console.print()
    print(f"[link={url}]Click here[/link]")
    console.print()
    console.print("*" * 100)


def print_creation_or_changes_to_validation_webhooks(api_config: ApiConfig):
    query = """
fields @timestamp, @message
| filter @logStream like "kube-apiserver-audit"
| filter verb in ["create", "update", "patch"] and responseStatus.code = 201
| filter objectRef.resource = "validatingwebhookconfigurations"
| sort @timestamp desc
    """

    url = generate_cloudwatch_query(
        api_config.region, query, [f"/aws/eks/{api_config.cluster}/cluster"]
    )

    console.print(
        "List creation of new or changes to validation webhooks", style="red"
    )
    console.print()
    print(f"[link={url}]Click here[/link]")
    console.print()
    console.print("*" * 100)


def print_create_update_delete_to_roles(api_config: ApiConfig):
    query = """
fields @timestamp, @message
| sort @timestamp desc
| filter objectRef.resource="roles" and verb in ["create", "update", "patch", "delete"]
    """

    url = generate_cloudwatch_query(
        api_config.region, query, [f"/aws/eks/{api_config.cluster}/cluster"]
    )

    console.print(
        "List create, update, delete operations to Roles", style="red"
    )
    console.print()
    print(f"[link={url}]Click here[/link]")
    console.print()
    console.print("*" * 100)


def print_create_update_delete_to_role_bindings(api_config: ApiConfig):
    query = """
fields @timestamp, @message
| sort @timestamp desc
| filter objectRef.resource="rolebindings" and verb in ["create", "update", "patch", "delete"]
    """

    url = generate_cloudwatch_query(
        api_config.region, query, [f"/aws/eks/{api_config.cluster}/cluster"]
    )

    console.print(
        "List create, update, delete operations to RoleBindings", style="red"
    )
    console.print()
    print(f"[link={url}]Click here[/link]")
    console.print()
    console.print("*" * 100)


def print_create_update_delete_to_cluster_roles(api_config: ApiConfig):
    query = """
fields @timestamp, @message
| sort @timestamp desc
| filter objectRef.resource="clusterroles" and verb in ["create", "update", "patch", "delete"]
    """

    url = generate_cloudwatch_query(
        api_config.region, query, [f"/aws/eks/{api_config.cluster}/cluster"]
    )

    console.print(
        "List create, update, delete operations to ClusterRoles", style="red"
    )
    console.print()
    print(f"[link={url}]Click here[/link]")
    console.print()
    console.print("*" * 100)


def print_create_update_delete_to_cluster_role_bindings(api_config: ApiConfig):
    query = """
fields @timestamp, @message
| sort @timestamp desc
| filter objectRef.resource="clusterrolebindings" and verb in ["create", "update", "patch", "delete"]
    """

    url = generate_cloudwatch_query(
        api_config.region, query, [f"/aws/eks/{api_config.cluster}/cluster"]
    )

    console.print(
        "List create, update, delete operations to ClusterRoleBindings",
        style="red",
    )
    console.print()
    print(f"[link={url}]Click here[/link]")
    console.print()
    console.print("*" * 100)


def print_failed_anonymous_requests(api_config: ApiConfig):
    query = """
fields @timestamp, @message, sourceIPs.0
| sort @timestamp desc
| filter user.username="system:anonymous" and responseStatus.code in ["401", "403"]
    """

    url = generate_cloudwatch_query(
        api_config.region, query, [f"/aws/eks/{api_config.cluster}/cluster"]
    )

    console.print("List of failed anonymous requests", style="red")
    console.print()
    print(f"[link={url}]Click here[/link]")
    console.print()
    console.print("*" * 100)
