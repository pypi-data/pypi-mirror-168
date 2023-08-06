from rich.console import Console

from ...report.print import (
    print_pod_table,
)
from ...helpers import ApiConfig

console = Console()


def disallow_container_socket_mount(api_config: ApiConfig):
    offenders = []

    sockets = [
        "/var/run/docker.sock",
        "/var/run/containerd.sock",
        "/var/run/crio.sock",
    ]

    for pod in api_config.pods:
        for volume in pod.spec.volumes:
            if volume.host_path and volume.host_path.path in sockets:
                offenders.append(pod)

    if offenders:
        print_pod_table(offenders, "Container socket mounts are not allowed")

    return offenders


def disallow_host_path_or_make_it_read_only(api_config: ApiConfig):
    offenders = []

    for pod in api_config.pods:
        for volume in pod.spec.volumes:
            if volume.host_path:
                offenders.append(pod)

    if offenders:
        print_pod_table(
            offenders,
            "Restrict the use of hostpath or make it read-only if you have to use it",
        )

    return offenders


def set_requests_limits_for_containers(api_config: ApiConfig):
    offenders = []

    for pod in api_config.pods:
        for container in pod.spec.containers:
            if not (
                container.resources.limits and container.resources.requests
            ):
                offenders.append(pod)

    if offenders:
        print_pod_table(
            offenders,
            "Set requests and limits for each container to avoid resource contention",
        )

    return offenders


def disallow_privilege_escalation(api_config: ApiConfig):
    offenders = []

    for pod in api_config.pods:
        if not hasattr(pod.spec.security_context, "allow_privilege_escalation"):
            offenders.append(pod)

    if offenders:
        print_pod_table(
            offenders, "Set allowPrivilegeEscalation in the pod spec to false"
        )

    return offenders


def check_read_only_root_file_system(api_config: ApiConfig):
    offenders = []

    for pod in api_config.pods:
        if not hasattr(pod.spec.security_context, "read_only_root_filesystem"):
            offenders.append(pod)

    if offenders:
        print_pod_table(
            offenders, "Configure your images with a read-only root file system"
        )

    return offenders
