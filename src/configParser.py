import os

import yaml


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

    print("Index".ljust(10) + "Name".ljust(20) + "Server".ljust(30))

    for i, (name, server) in enumerate(clusters, start=1):
        print(f"{i:<10}{name:<20}{server:<30}")
