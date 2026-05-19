from kubernetes import client
from kubernetes.client.exceptions import ApiException
from tabulate import tabulate
from urllib3.exceptions import MaxRetryError

from src.configParser import get_context_info, load_kubeconfig
from src.resolve import resolve_namespaces
from src.toDict import pods_to_dict


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
        parents=parents or [],
    )
    parse_all_pods.set_defaults(func=list_all_pods)

    # List all pods that are not in a running phase
    parse_not_running = pods_subparsers.add_parser(
        "not-running",
        help="List pods that are not running",
        parents=parents or [],
    )
    parse_not_running.set_defaults(func=list_not_running_pods)


def get_namespaced_pods(namespace):
    v1 = client.CoreV1Api()
    try:
        # Setting a low connection timeout to fail fast since we are unable to control
        # the amount of retries as mentioned in this issue: https://github.com/kubernetes-client/python/issues/962
        # 0.2s connect timeout (connection shouldn't take longer than 500ms)
        # 2s read timeout
        resp = v1.list_namespaced_pod(namespace=namespace, _request_timeout=(0.2, 2))
        # v1.list_pod_for_all_namespaces(watch=False, _request_timeout=(0.2, 2))
        return resp.items
    except Exception as e:
        # Better Error formatting in cases where a user might hit the retry limit
        if isinstance(e, MaxRetryError):
            root = e.reason
            host = e.pool.host
            url = e.url
            raise Exception(
                f"Failed to reach Kubernetes API at {host}\nEndpoint: {url}\nCause: {type(root).__name__}\nDetail: {root}"
            )
        raise e


def get_namespaced_pod_rows(args):
    load_kubeconfig(args)
    context_info = get_context_info(args)

    namespaces = resolve_namespaces(args, context_info)

    all_rows = []
    failed_namespaces = []

    # Building list of pods to be used by render_table()
    for ns in namespaces:
        try:
            pods = get_namespaced_pods(ns)
            rows = pods_to_dict(pods)
            all_rows.extend(rows)
        except ApiException as e:
            failed_namespaces.append((ns, e))

    return all_rows, failed_namespaces


def render_table(rows):
    table = []
    for i, pod in enumerate(rows, start=1):
        table.append([i, pod["name"], pod["namespace"], pod["status"]])

    print(tabulate(table, headers=["#", "Name", "Namespace", "Status"]))
    print(f"Total amount of pods: {len(rows)}")


# --- Command Line Interface ---


def list_all_pods(args):
    try:
        rows, failed_namespaces = get_namespaced_pod_rows(args)
        render_table(rows)

        # Beauty line!
        print()
        if failed_namespaces:
            for ns, e in failed_namespaces:
                if e.status == 403:
                    print(f"Warning {e.status}: cannot access namespace {ns}")
                else:
                    print(
                        f"Error status: {e.status} - Error {e.reason} for namespace {ns}"
                    )
    except Exception as e:
        print(f"Error: {e}")
        exit(1)


def list_not_running_pods(args):
    try:
        rows, failed_namespaces = get_namespaced_pod_rows(args)
        not_running_rows = [row for row in rows if row["status"] != "Running"]
        render_table(not_running_rows)

        # Beauty line!
        print()
        if failed_namespaces:
            for ns, e in failed_namespaces:
                if e.status == 403:
                    print(f"Warning {e.status}: cannot access namespace {ns}")
                else:
                    print(
                        f"Error status: {e.status} - Error {e.reason} for namespace {ns}"
                    )
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
