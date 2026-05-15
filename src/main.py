import argparse
import os
import sys

from src.configParser import parse_config


def main():
    parser = argparse.ArgumentParser(description="Kubernetes Viewer CLI")
    subparsers = parser.add_subparsers(dest="command", required=True, metavar="")

    kubeconfig_parser = subparsers.add_parser(
        "kubeconfig", help="List information about the kubeconfig"
    )
    kubeconfig_parser.add_argument("--configfile", default=None)
    kubeconfig_parser.set_defaults(func=parse_config)

    # friendly fallback to help if no command is provided
    if len(sys.argv) == 1:
        parser.print_help()
        return

    args = parser.parse_args()

    # trying to read kubeconfig from command line or env var and expanding '~' to user path
    config_path = (
        os.path.expanduser(args.configfile)
        if args.configfile
        else os.path.expanduser(os.environ.get("KUBECONFIG", ""))
    )

    if not config_path:
        print("No config file provided")
        parser.print_help()
        return

    args.func(config_path)


if __name__ == "__main__":
    main()
