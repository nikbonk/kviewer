import argparse
import sys

import src.configParser
import src.podParser
import src.subjectParser


def build_parser():
    # Root parser
    parser = argparse.ArgumentParser(description="Kubernetes Viewer CLI")

    # shared "parent" parser
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "-c",
        "--configfile",
        default=None,
        help="Path to the kubeconfig file",
        metavar="",
    )

    # Subcommand registry
    subparsers = parser.add_subparsers(dest="command", required=True, metavar="")

    # Functions register their subcommands
    src.configParser.setup_args(subparsers, parents=[common])
    src.podParser.setup_args(subparsers, parents=[common])
    src.subjectParser.setup_subject_args(subparsers, parents=[common])

    return parser


def main():
    parser = build_parser()

    # Show help if no subcommand is provided
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    # Parse CLI input
    args = parser.parse_args()

    # let argparse dispatch the command via the registered function
    # each subcommand attaches its own function via `set_defaults`
    args.func(args)


if __name__ == "__main__":
    main()
