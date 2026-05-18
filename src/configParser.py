import os

import yaml
from kubernetes import config
from tabulate import tabulate


def setup_args(subparsers, parents=None):
    # register the kubeconfig subcommand
    parser_kubeconfig = subparsers.add_parser(
        "kubeconfig",
        help="List information about the kubeconfig",
        parents=parents or [],
    )

    parser_kubeconfig_context = subparsers.add_parser(
        "kubeconfig-context",
        help="List information about the current kubeconfig context",
        parents=parents or [],
    )

    # Attach the `handle_kubeconfig` function to the kubeconfig subcommand
    parser_kubeconfig.set_defaults(func=handle_kubeconfig)

    # Attach the `get_context_info` function to the kubeconfig-context subcommand
    parser_kubeconfig_context.set_defaults(func=get_context_info)


def resolve_config_path(args):
    # Resolve the config file path from the command line arguments, environment variable, or default path
    candidates = [args.configfile, os.environ.get("KUBECONFIG"), "~/.kube/config"]

    for path in candidates:
        if path:
            expanded_path = os.path.expanduser(path)
            if os.path.exists(expanded_path):
                return expanded_path
    return None


def get_context_info(args):
    config_file = resolve_config_path(args)

    if not config_file:
        print(
            "No kubeconfig file found.\n"
            "Make sure KUBECONFIG is set or use --configfile."
        )
        exit(1)

    with open(config_file, "r") as f:
        data = yaml.safe_load(f)

    current_context = data.get("current-context")

    for ctx in data.get("contexts", []):
        if ctx["name"] == current_context:
            namespace = ctx["context"].get("namespace", "default")
            cluster = ctx["context"]["cluster"]
            user = ctx["context"]["user"]
            context_info = {
                "namespace": namespace,
                "cluster": cluster,
                "user": user,
            }
            return context_info

    return None


def parse_kubeconfig(config_file: str):
    with open(config_file, "r") as f:
        data = yaml.safe_load(f)

    return [
        (c.get("name"), c.get("cluster", {}).get("server"))
        for c in data.get("clusters", [])
    ]


def handle_kubeconfig(args):
    # Fail fast if no config file is found
    config_file = resolve_config_path(args)
    if not config_file:
        print(
            "No kubeconfig file found.\nMake sure KUBECONFIG is set or use --configfile."
        )
        exit(1)

    clusters = parse_kubeconfig(config_file)

    table = []
    i = 0
    for i, (name, server) in enumerate(clusters, start=1):
        table.append([i, name, server])

    print(tabulate(table, headers=["#", "Name", "Server"]))
    print(f"Total amount of clusters: {i}")


# Load the kubeconfig file to be used by the Kubernetes client
def load_kubeconfig(args):
    config_file = resolve_config_path(args)
    if not config_file:
        print(
            "No kubeconfig file found.\nMake sure KUBECONFIG is set or use --configfile."
        )
        exit(1)
    config.load_kube_config(config_file)
