from collections import Counter

import boto3
from rich.console import Console
from kubernetes import client

from ...helpers import ApiConfig
from ...report.print import (
    print_role_table,
    print_instance_table,
    print_pod_table,
    print_workload_table,
)

console = Console()


def restrict_wildcard_for_roles(api_config: ApiConfig):
    """
    https://aws.github.io/aws-eks-best-practices/security/docs/iam/#employ-least-privileged-access-when-creating-rolebindings-and-clusterrolebindings
    """

    offenders = []

    for role in api_config.roles:
        for rule in role.rules:
            if "*" in rule.verbs:
                offenders.append(role)
            if "*" in rule.resources:
                offenders.append(role)

    if offenders:
        print_role_table(
            offenders, "Roles should not have '*' in Verbs or Resources", "Role"
        )
    return offenders


def restrict_wildcard_for_cluster_roles(api_config: ApiConfig):
    """
    https://aws.github.io/aws-eks-best-practices/security/docs/iam/#employ-least-privileged-access-when-creating-rolebindings-and-clusterrolebindings
    """

    offenders = []

    for role in api_config.cluster_roles:
        for rule in role.rules:
            if "*" in rule.verbs:
                offenders.append(role)
            if rule.resources and "*" in rule.resources:
                offenders.append(role)

    if offenders:
        print_role_table(
            offenders,
            "ClusterRoles should not have '*' in Verbs or Resources",
            "ClusterRole",
        )
    return offenders


def check_endpoint_public_access(api_config: ApiConfig):
    client = boto3.client("eks", region_name=api_config.region)
    cluster_metadata = client.describe_cluster(name=api_config.cluster)
    endpoint_access = cluster_metadata["cluster"]["resourcesVpcConfig"][
        "endpointPublicAccess"
    ]
    if endpoint_access:
        console.print("EKS Cluster Endpoint is not Private", style="red")
        console.print()
        console.print("*" * 100)
        return True


def check_aws_node_daemonset_service_account(api_config: ApiConfig):
    daemonset = client.AppsV1Api().read_namespaced_daemon_set(
        name="aws-node", namespace="kube-system"
    )

    if daemonset.spec.template.spec.service_account_name == "aws-node":
        console.print("Update the aws-node daemonset to use IRSA", style="red")
        console.print()
        console.print("*" * 100)
        return True


def check_access_to_instance_profile(api_config: ApiConfig):
    client = boto3.client("ec2", region_name=api_config.region)
    offenders = []
    instance_metadata = client.describe_instances(
        Filters=[
            {
                "Name": "tag:aws:eks:cluster-name",
                "Values": [
                    api_config.cluster,
                ],
            },
        ]
    )
    for instance in instance_metadata["Reservations"]:
        if (
            instance["Instances"][0]["MetadataOptions"][
                "HttpPutResponseHopLimit"
            ]
            == 2
        ):
            offenders.append(instance)

    if offenders:
        print_instance_table(
            offenders,
            "Restrict access to the instance profile assigned to the worker node",
        )
    return offenders


def disable_service_account_token_mounts(api_config: ApiConfig):
    offenders = []

    for pod in api_config.pods:
        if pod.spec.automount_service_account_token != False:
            offenders.append(pod)

    if offenders:
        print_pod_table(
            offenders, "Auto-mounting of Service Account tokens is not allowed"
        )
    return offenders


def disable_run_as_root_user(api_config: ApiConfig):
    offenders = []

    for pod in api_config.pods:
        security_context = pod.spec.security_context
        if (
            not security_context.run_as_group
            and not security_context.run_as_user
        ):
            offenders.append(pod)

    if offenders:
        print_pod_table(offenders, "Running as root is not allowed")

    return offenders


def disable_anonymous_access_for_roles(api_config: ApiConfig):
    offenders = []

    for role_binding in api_config.role_bindings:
        if role_binding.subjects:
            for subject in role_binding.subjects:
                if (
                    subject.name == "system:unauthenticated"
                    or subject.name == "system:anonymous"
                ):
                    offenders.append(role_binding)

    if offenders:
        print_role_table(
            offenders,
            "Don't bind roles to system:anonymous or system:unauthenticated groups",
            "RoleBinding",
        )
    return offenders


def disable_anonymous_access_for_cluster_roles(api_config: ApiConfig):
    offenders = []

    for cluster_role_binding in api_config.cluster_role_bindings:
        if cluster_role_binding.subjects:
            for subject in cluster_role_binding.subjects:
                if (
                    subject.name == "system:unauthenticated"
                    or subject.name == "system:anonymous"
                ):
                    offenders.append(cluster_role_binding)

    if offenders:
        print_role_table(
            offenders,
            "Don't bind clusterroles to system:anonymous or system:unauthenticated groups",
            "ClusterRoleBinding",
        )

    return offenders


def use_dedicated_service_accounts_for_each_deployment(api_config: ApiConfig):
    offenders = []

    count = Counter(
        [
            i.spec.template.spec.service_account_name
            for i in api_config.deployments
        ]
    )
    repeated_service_accounts = {
        x: count for x, count in count.items() if count > 1
    }

    for k, v in repeated_service_accounts.items():
        for deployment in api_config.deployments:
            if k == deployment.spec.template.spec.service_account_name:
                offenders.append(deployment)

    if offenders:
        print_workload_table(
            offenders,
            "Don't share service accounts between Deployments",
            "Deployment",
        )

    return offenders


def use_dedicated_service_accounts_for_each_stateful_set(api_config: ApiConfig):
    offenders = []

    count = Counter(
        [
            i.spec.template.spec.service_account_name
            for i in api_config.stateful_sets
        ]
    )
    repeated_service_accounts = {
        x: count for x, count in count.items() if count > 1
    }

    for k, v in repeated_service_accounts.items():
        for deployment in api_config.stateful_sets:
            if k == deployment.spec.template.spec.service_account_name:
                offenders.append(deployment)

    if offenders:
        print_workload_table(
            offenders,
            "Don't share service accounts between StatefulSets",
            "StatefulSet",
        )

    return offenders


def use_dedicated_service_accounts_for_each_daemon_set(api_config: ApiConfig):
    offenders = []

    count = Counter(
        [
            i.spec.template.spec.service_account_name
            for i in api_config.daemon_sets
        ]
    )
    repeated_service_accounts = {
        x: count for x, count in count.items() if count > 1
    }

    for k, v in repeated_service_accounts.items():
        for deployment in api_config.daemon_sets:
            if k == deployment.spec.template.spec.service_account_name:
                offenders.append(deployment)

    if offenders:
        print_workload_table(
            offenders,
            "Don't share service accounts between DaemonSets",
            "DaemonSet",
        )

    return offenders
