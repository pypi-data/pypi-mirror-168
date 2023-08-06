# `eks-best-practices-cli`

#### This is not an officially supported AWS product.

Runs checks to see if an EKS cluster follows [EKS Best Practices](https://aws.github.io/aws-eks-best-practices/).


**Quick Start**:
```
python3 -m venv /tmp/.venv
source /tmp/.venv/bin/activate
pip install eks-best-practices-cli
```

**Configuration File**:

There is a configuration file that you have to provide which allows customization of which checks to run as well as namespaces to be skipped by the checks. Following is a sample config file.


```
[namespaces]
ignored = [
    "kube-node-lease",
    "kube-public",
    "kube-system",
    "kube-apiserver"
    ]

[rules]
run = [
    "disable_anonymous_access_for_cluster_roles",
    "disable_anonymous_access_for_roles",
    "restrict_wildcard_for_roles",
    "restrict_wildcard_for_cluster_roles",
    "check_endpoint_public_access",
    "check_aws_node_daemonset_service_account",
    "check_access_to_instance_profile",
    "disable_service_account_token_mounts",
    "disable_run_as_root_user",
    "use_dedicated_service_accounts_for_each_deployment",
    "use_dedicated_service_accounts_for_each_stateful_set",
    "use_dedicated_service_accounts_for_each_daemon_set", 
    "disallow_container_socket_mount",
    "disallow_host_path_or_make_it_read_only",
    "set_requests_limits_for_containers",
    "disallow_privilege_escalation",
    "check_read_only_root_file_system", 
    "check_logs_are_enabled",
    "print_aws_auth_config_map_updates",
    "print_creation_or_changes_to_validation_webhooks",
    "print_create_update_delete_to_roles",
    "print_create_update_delete_to_cluster_role_bindings",
    "print_create_update_delete_to_cluster_roles",
    "print_create_update_delete_to_role_bindings",
    "print_failed_anonymous_requests",
    "check_default_deny_policy_exists",
    "ensure_namespace_quotas_exist",
    "check_vpc_flow_logs",
    "use_encryption_with_aws_load_balancers"
    ]
```

**Usage**:

```console
eks-best-practices-cli [OPTIONS]
```

**Options**:

* `--region TEXT`: AWS Region [required]
* `--context TEXT`: Kubernetes context [required]
* `--config-path PATH`: Path to the config file [required]
* `--help`: Show this message and exit.

You can get the current kubernetes context by running:
```
kubectl config current-context
```

As an example:

```
check-eks-best-practices --region us-east-1 --context arn:aws:eks:us-east-1:some-account-id:cluster/some-cluster-name --config-path /path/to/config.ini
```

## For Developers

**Prerequisites**:

* This cli uses poetry. Follow instructions that are outlined [here](https://python-poetry.org/docs/) to install poetry.


**Installation**:

```console
git clone git@github.com:dorukozturk/eks-best-practices-cli.git
cd eks-best-practices-cli
poetry install
```


**Running Tests**:

```console
poetry shell
pytest --cov=eks_best_practices_cli tests/
```

