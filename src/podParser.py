import sys

from kubernetes import client
from tabulate import tabulate

from src.configParser import load_kubeconfig


def setup_args(subparsers, parents=None):

    parse_pods = subparsers.add_parser(
        "pods",
        help="List information about all pods",
        parents=parents or [],
    )

    # register new subparser to handle different subcommands for listing pods
    pods_subparsers = parse_pods.add_subparsers(
        dest="pods_subcommand",
        help="Refine the list of pods",
        required=True,
        metavar="",
    )

    # Just list all pods
    parse_all_pods = pods_subparsers.add_parser(
        "all",
        help="List all pods",
    )
    parse_all_pods.set_defaults(func=list_all_pods)

    # List all pods that are not in a running phase
    parse_not_running = pods_subparsers.add_parser(
        "not-running",
        help="List pods that are not running",
    )
    parse_not_running.set_defaults(func=list_not_running_pods)

    # Show help if no subcommand is provided
    if len(sys.argv) == 2:
        parse_pods.print_help()
        sys.exit(0)


def list_all_pods(args):
    try:
        load_kubeconfig(args)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

    v1 = client.CoreV1Api()

    pods = v1.list_pod_for_all_namespaces(watch=False)

    table = []
    i = 0
    for pod in pods.items:
        i += 1
        table.append([i, pod.metadata.name, pod.metadata.namespace])

    print(tabulate(table, headers=["#", "Name", "Namespace"]))
    print(f"Total amount of pods: {i}")


def list_not_running_pods(args):
    try:
        load_kubeconfig(args)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

    v1 = client.CoreV1Api()

    pods = v1.list_pod_for_all_namespaces(watch=False)

    table = []
    i = 0
    for pod in pods.items:
        if pod.status.phase != "Running":
            i += 1
            table.append(
                [i, pod.metadata.name, pod.metadata.namespace, pod.status.phase]
            )

    print(tabulate(table, headers=["#", "Name", "Namespace", "Status"]))
    print(f"Total amount of not running pods: {i}")
