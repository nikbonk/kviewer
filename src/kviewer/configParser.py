import os

import yaml
from kubernetes import config

from .toTable import build_cluster_table, render


def setup_args(subparsers, parents=None):
    # register the kubeconfig subcommand
    parser_kubeconfig = subparsers.add_parser(
        "kubeconfig",
        help="List information about the kubeconfig",
        parents=parents or [],
    )

    # Attach the `handle_kubeconfig` function to the kubeconfig subcommand
    parser_kubeconfig.set_defaults(func=handle_kubeconfig)


# Resolve the config file path from the command line arguments, environment variable, or default path
def resolve_config_path(args):
    candidates = [args.configfile, os.environ.get("KUBECONFIG"), "~/.kube/config"]

    for path in candidates:
        if path:
            expanded_path = os.path.expanduser(path)
            if os.path.exists(expanded_path):
                return expanded_path
    return None


# Return a list of (name, server) tuples from the kubeconfig file to be rendered by the `kubeconfig` subcommand
def parse_kubeconfig(config_file: str):
    with open(config_file, "r") as f:
        data = yaml.safe_load(f)

    return [
        (c.get("name"), c.get("cluster", {}).get("server"))
        for c in data.get("clusters", [])
    ]


# Retrieve some useful information out of the current current-context to be used by the
# Kubernetes client for something like fallback namespace resolution
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


# Load the kubeconfig file to be used by the Kubernetes client
def load_kubeconfig(args):
    config_file = resolve_config_path(args)
    if not config_file:
        print(
            "No kubeconfig file found.\nMake sure KUBECONFIG is set or use --configfile."
        )
        exit(1)
    config.load_kube_config(config_file)


# --- Command Line Interface ---
def handle_kubeconfig(args):
    # Fail fast if no config file is found
    config_file = resolve_config_path(args)
    if not config_file:
        print(
            "No kubeconfig file found.\nMake sure KUBECONFIG is set or use --configfile."
        )
        exit(1)

    clusters = parse_kubeconfig(config_file)
    output = build_cluster_table(clusters)
    render(output, args)
