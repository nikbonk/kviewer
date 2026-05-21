from kubernetes import client

from .configParser import load_kubeconfig
from .toTable import build_node_table, render


def setup_args(subparsers, parents=None):

    parse_nodes = subparsers.add_parser(
        "nodes",
        help="List information about the nodes",
        parents=parents or [],
    )

    parse_nodes.set_defaults(func=list_nodes)


# --- Command Line Interface ---


def list_nodes(args):
    load_kubeconfig(args)
    v1 = client.CoreV1Api()
    nodes = v1.list_node()
    output = build_node_table(nodes.items)
    render(output, args)
