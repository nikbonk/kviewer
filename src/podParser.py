from kubernetes import client
from tabulate import tabulate

from src.configParser import load_kubeconfig


def setup_args(subparsers, parents=None):
    # register the kubeconfig subcommand
    parse_pods = subparsers.add_parser(
        "pods",
        help="List information about all pods",
        parents=parents or [],
    )

    # Attach the `list_pods` function to the kubeconfig subcommand
    parse_pods.set_defaults(func=list_pods)


def list_pods(args):
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
