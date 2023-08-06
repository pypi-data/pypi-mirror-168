import configparser
from datetime import datetime, timedelta
from pathlib import Path
from typing import List
from urllib.parse import quote

from kubernetes import client

import typer


def resolve_config(path: Path):
    if path.is_file():
        config = configparser.ConfigParser()
        config.read(path)
        return config
    elif path.is_dir():
        print("Config should be a file not a directory")
        raise typer.Exit()
    elif not path.exists():
        print("The config doesn't exist")
        raise typer.Exit()


def _generate_aws_cloudwatch_log_insights_url(query_parameters, aws_region):
    """
    https://stackoverflow.com/a/70506522
    """

    def quote_string(input_str):
        return f"""{quote(input_str, safe="~()'*").replace('%', '*')}"""

    def quote_list(input_list):
        quoted_list = ""
        for item in input_list:
            if isinstance(item, str):
                item = f"'{item}"

            quoted_list += f"~{item}"
        return f"({quoted_list})"

    params = []
    for key, value in query_parameters.items():
        if key == "editorString":
            value = "'" + quote(value)
            value = value.replace("%", "*")
        elif isinstance(value, str):
            value = "'" + value
        if isinstance(value, bool):
            value = str(value).lower()
        elif isinstance(value, list):
            value = quote_list(value)
        params += [key, str(value)]

    object_string = quote_string("~(" + "~".join(params) + ")")
    scaped_object = quote(object_string, safe="*").replace("~", "%7E")
    with_query_detail = "?queryDetail=" + scaped_object
    result = quote(with_query_detail, safe="*").replace("%", "$")

    final_url = f"https://{aws_region}.console.aws.amazon.com/cloudwatch/home?region={aws_region}#logsV2:logs-insights{result}"

    return final_url


def generate_cloudwatch_query(region, query, log_groups):

    query_parameters = {
        "end": datetime.utcnow().isoformat(timespec="milliseconds") + "Z",
        "start": (datetime.utcnow() - timedelta(days=2)).isoformat(
            timespec="milliseconds"
        )
        + "Z",
        "timeType": "ABSOLUTE",
        "unit": "seconds",
        "editorString": query,
        "isLiveTrail": False,
        "source": log_groups,
    }

    return _generate_aws_cloudwatch_log_insights_url(
        query_parameters=query_parameters, aws_region=region
    )


class ApiConfig(object):
    def __init__(
        self,
        region,
        context,
        ignored_namespaces,
    ):
        self.region = region
        self.cluster = context.split("cluster/")[1]
        self.namespaces = self.filter_ignored_namespaces(
            client.CoreV1Api().list_namespace().items, ignored_namespaces
        )
        self.resource_quotas = self.filter_resources(
            client.CoreV1Api().list_resource_quota_for_all_namespaces().items,
            ignored_namespaces,
        )
        self.roles = self.filter_resources(
            client.RbacAuthorizationV1Api()
            .list_role_for_all_namespaces()
            .items,
            ignored_namespaces,
        )
        self.cluster_roles = (
            client.RbacAuthorizationV1Api().list_cluster_role().items
        )
        self.pods = self.filter_resources(
            client.CoreV1Api().list_pod_for_all_namespaces().items,
            ignored_namespaces,
        )
        self.role_bindings = self.filter_resources(
            client.RbacAuthorizationV1Api()
            .list_role_binding_for_all_namespaces()
            .items,
            ignored_namespaces,
        )
        self.cluster_role_bindings = (
            client.RbacAuthorizationV1Api().list_cluster_role_binding().items
        )
        self.deployments = self.filter_resources(
            client.AppsV1Api().list_deployment_for_all_namespaces().items,
            ignored_namespaces,
        )
        self.daemon_sets = self.filter_resources(
            client.AppsV1Api().list_daemon_set_for_all_namespaces().items,
            ignored_namespaces,
        )
        self.stateful_sets = self.filter_resources(
            client.AppsV1Api().list_stateful_set_for_all_namespaces().items,
            ignored_namespaces,
        )
        self.network_policies = self.filter_resources(
            client.NetworkingV1Api()
            .list_network_policy_for_all_namespaces()
            .items,
            ignored_namespaces,
        )
        self.services = self.filter_resources(
            client.CoreV1Api()
            .list_service_for_all_namespaces()
            .items,
            ignored_namespaces,
        )

    def filter_ignored_namespaces(self, namespaces: List, ignored_ns: List):
        return [i for i in namespaces if i.metadata.name not in ignored_ns]

    def filter_resources(self, resources: List, ignored_ns: List):
        return [i for i in resources if i.metadata.namespace not in ignored_ns]
