# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eks_best_practices_cli',
 'eks_best_practices_cli.report',
 'eks_best_practices_cli.security',
 'eks_best_practices_cli.security.auditing_logging',
 'eks_best_practices_cli.security.iam',
 'eks_best_practices_cli.security.multi_tenancy',
 'eks_best_practices_cli.security.network_security',
 'eks_best_practices_cli.security.pod_security']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.24.63,<2.0.0',
 'kubernetes>=24.2.0,<25.0.0',
 'rich>=12.5.1,<13.0.0',
 'typer-cli>=0.0.12,<0.0.13']

entry_points = \
{'console_scripts': ['check-eks-best-practices = '
                     'eks_best_practices_cli.main:app']}

setup_kwargs = {
    'name': 'eks-best-practices-cli',
    'version': '0.1.1',
    'description': '',
    'long_description': '# `eks-best-practices-cli`\n\n#### This is not an officially supported AWS product.\n\nRuns checks to see if an EKS cluster follows [EKS Best Practices](https://aws.github.io/aws-eks-best-practices/).\n\n\n**Quick Start**:\n```\npython3 -m venv /tmp/.venv\nsource /tmp/.venv/bin/activate\npip install eks-best-practices-cli\n```\n\n**Configuration File**:\n\nThere is a configuration file that you have to provide which allows customization of which checks to run as well as namespaces to be skipped by the checks. Following is a sample config file.\n\n\n```\n[namespaces]\nignored = [\n    "kube-node-lease",\n    "kube-public",\n    "kube-system",\n    "kube-apiserver"\n    ]\n\n[rules]\nrun = [\n    "disable_anonymous_access_for_cluster_roles",\n    "disable_anonymous_access_for_roles",\n    "restrict_wildcard_for_roles",\n    "restrict_wildcard_for_cluster_roles",\n    "check_endpoint_public_access",\n    "check_aws_node_daemonset_service_account",\n    "check_access_to_instance_profile",\n    "disable_service_account_token_mounts",\n    "disable_run_as_root_user",\n    "use_dedicated_service_accounts_for_each_deployment",\n    "use_dedicated_service_accounts_for_each_stateful_set",\n    "use_dedicated_service_accounts_for_each_daemon_set", \n    "disallow_container_socket_mount",\n    "disallow_host_path_or_make_it_read_only",\n    "set_requests_limits_for_containers",\n    "disallow_privilege_escalation",\n    "check_read_only_root_file_system", \n    "check_logs_are_enabled",\n    "print_aws_auth_config_map_updates",\n    "print_creation_or_changes_to_validation_webhooks",\n    "print_create_update_delete_to_roles",\n    "print_create_update_delete_to_cluster_role_bindings",\n    "print_create_update_delete_to_cluster_roles",\n    "print_create_update_delete_to_role_bindings",\n    "print_failed_anonymous_requests",\n    "check_default_deny_policy_exists",\n    "ensure_namespace_quotas_exist",\n    "check_vpc_flow_logs",\n    "use_encryption_with_aws_load_balancers"\n    ]\n```\n\n**Usage**:\n\n```console\neks-best-practices-cli [OPTIONS]\n```\n\n**Options**:\n\n* `--region TEXT`: AWS Region [required]\n* `--context TEXT`: Kubernetes context [required]\n* `--config-path PATH`: Path to the config file [required]\n* `--help`: Show this message and exit.\n\nYou can get the current kubernetes context by running:\n```\nkubectl config current-context\n```\n\nAs an example:\n\n```\ncheck-eks-best-practices --region us-east-1 --context arn:aws:eks:us-east-1:some-account-id:cluster/some-cluster-name --config-path /path/to/config.ini\n```\n\n## For Developers\n\n**Prerequisites**:\n\n* This cli uses poetry. Follow instructions that are outlined [here](https://python-poetry.org/docs/) to install poetry.\n\n\n**Installation**:\n\n```console\ngit clone git@github.com:dorukozturk/eks-best-practices-cli.git\ncd eks-best-practices-cli\npoetry install\n```\n\n\n**Running Tests**:\n\n```console\npoetry shell\npytest --cov=eks_best_practices_cli tests/\n```\n\n',
    'author': 'Doruk Ozturk',
    'author_email': 'dozturk@amazon.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
