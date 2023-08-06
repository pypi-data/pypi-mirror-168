import json
from pathlib import Path

from kubernetes import config
from rich import print
import typer

from .security.iam.rules import (
    disable_anonymous_access_for_cluster_roles,
    disable_anonymous_access_for_roles,
    restrict_wildcard_for_roles,
    restrict_wildcard_for_cluster_roles,
    check_endpoint_public_access,
    check_aws_node_daemonset_service_account,
    check_access_to_instance_profile,
    disable_service_account_token_mounts,
    disable_run_as_root_user,
    use_dedicated_service_accounts_for_each_deployment,
    use_dedicated_service_accounts_for_each_stateful_set,
    use_dedicated_service_accounts_for_each_daemon_set,
)
from .security.pod_security.rules import (
    disallow_container_socket_mount,
    disallow_host_path_or_make_it_read_only,
    set_requests_limits_for_containers,
    disallow_privilege_escalation,
    check_read_only_root_file_system,
)
from .security.auditing_logging.rules import (
    check_logs_are_enabled,
    print_aws_auth_config_map_updates,
    print_creation_or_changes_to_validation_webhooks,
    print_create_update_delete_to_roles,
    print_create_update_delete_to_cluster_role_bindings,
    print_create_update_delete_to_cluster_roles,
    print_create_update_delete_to_role_bindings,
    print_failed_anonymous_requests,
)
from .security.network_security.rules import (
    check_default_deny_policy_exists,
    check_vpc_flow_logs,
    use_encryption_with_aws_load_balancers,
)
from .security.multi_tenancy.rules import ensure_namespace_quotas_exist
from .helpers import (
    ApiConfig,
    resolve_config,
)

app = typer.Typer()


@app.command()
def check_eks_best_practices(
    region: str = typer.Option(...),
    context: str = typer.Option(...),
    config_path: Path = typer.Option(...),
):
    """
    Run all the checks for best practices
    """
    app_config = resolve_config(config_path)
    ignored_namespaces = json.loads(app_config.get("namespaces", "ignored"))
    rules = json.loads(app_config.get("rules", "run"))
    config.load_kube_config(context=context)

    api_config = ApiConfig(region, context, ignored_namespaces)

    print()
    print("Ignoring namespaces: ")
    print(ignored_namespaces)
    print()
    print("*" * 100)

    for rule in rules:
        try:
            globals()[rule](api_config)
        except KeyError:
            raise ValueError(f"{rule} is not part of the rules")
