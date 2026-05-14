import argparse
import os
import sys

from src.configParser import parse_config


def main():
    parser = argparse.ArgumentParser(description="Kubernetes Viewer CLI")
    subparsers = parser.add_subparsers(dest="command", required=True, metavar="")

    list_parser = subparsers.add_parser("list", help="List resources")
    list_parser.add_argument("--configfile", default=None)
    list_parser.set_defaults(func=parse_config)

    if len(sys.argv) == 1:
        parser.print_help()
        return

    args = parser.parse_args()

    config_path = args.configfile or os.environ.get("KUBECONFIG")

    if not config_path:
        print("No config file provided")
        parser.print_help()
        return

    args.func(config_path)


if __name__ == "__main__":
    main()
