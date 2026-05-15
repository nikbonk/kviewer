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

    # Attach the `handle_kubeconfig` function to the kubeconfig subcommand
    parser_kubeconfig.set_defaults(func=handle_kubeconfig)


def resolve_config_path(args):
    # Resolve the config file path from the command line arguments, environment variable, or default path
    candidates = [args.configfile, os.environ.get("KUBECONFIG"), "~/.kube/config"]

    for path in candidates:
        if path:
            expanded_path = os.path.expanduser(path)
            if os.path.exists(expanded_path):
                return expanded_path
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
