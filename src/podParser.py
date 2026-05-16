import sys

from kubernetes import client
from tabulate import tabulate
from urllib3.exceptions import MaxRetryError

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
        "not-running", help="List pods that are not running", parents=parents or []
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

    try:
        # Setting a low connection timeout to fail fast since we are unable to control
        # the amount of retries as mentioned in this issue: https://github.com/kubernetes-client/python/issues/962
        # 0.2s connect timeout (connection shouldn't take longer than 500ms)
        # 2s read timeout
        pods = v1.list_pod_for_all_namespaces(watch=False, _request_timeout=(0.2, 2))
    except Exception as e:
        # Better Error formatting in cases where a user might hit the retry limit
        if isinstance(e, MaxRetryError):
            root = e.reason
            host = e.pool.host
            url = e.url

            print(f"Failed to reach Kubernetes API at {host}")
            print(f"Endpoint: {url}")
            print(f"Cause: {type(root).__name__}")
            print(f"Detail: {root}")
            exit(1)

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

    try:
        # Setting a low connection timeout to fail fast since we are unable to control
        # the amount of retries as mentioned in this issue: https://github.com/kubernetes-client/python/issues/962
        # 0.2s connect timeout (connection shouldn't take longer than 500ms)
        # 2s read timeout
        pods = v1.list_pod_for_all_namespaces(watch=False, _request_timeout=(0.2, 2))
    except Exception as e:
        # Better Error formatting in cases where a user might hit the retry limit
        if isinstance(e, MaxRetryError):
            root = e.reason
            host = e.pool.host
            url = e.url

            print(f"Failed to reach Kubernetes API at {host}")
            print(f"Endpoint: {url}")
            print(f"Cause: {type(root).__name__}")
            print(f"Detail: {root}")
            exit(1)

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
