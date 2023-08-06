from rich.console import Console

from ...helpers import ApiConfig

from ...report.print import (
    print_namespace_table,
)

console = Console()


def ensure_namespace_quotas_exist(api_config: ApiConfig):

    offenders = [i.metadata.name for i in api_config.namespaces]

    for quota in api_config.resource_quotas:
        offenders.remove(quota.metadata.namespace)

    if offenders:
        print_namespace_table(
            offenders,
            "Namespaces should have quotas assigned",
        )

    return offenders
