from kubernetes import client
from tabulate import tabulate

from .configParser import get_context_info, load_kubeconfig
from .resolve import resolve_namespaces


def setup_subject_args(subparsers, parents=None):
    p = subparsers.add_parser(
        "subject",
        help="List subject powers",
        parents=parents or [],
    )
    p.set_defaults(func=get_subject)


def build_subject_rows(rules):
    rows = []

    for r in rules:
        verbs = "/".join(sorted(r.verbs or []))

        for res in r.resources or []:
            rows.append(
                {
                    "name": res,
                    "verbs": verbs,
                }
            )

    return rows


def render_subject_table(rows):
    table = [[i, row["name"], row["verbs"]] for i, row in enumerate(rows, start=1)]

    print(tabulate(table, headers=["#", "Resource", "Verbs"]))


def get_subject(args):
    load_kubeconfig(args)

    namespaces = resolve_namespaces(args, get_context_info(args))
    auth = client.AuthorizationV1Api()

    for ns in namespaces:
        review = auth.create_self_subject_rules_review(
            body=client.V1SelfSubjectRulesReview(
                spec=client.V1SelfSubjectRulesReviewSpec(namespace=ns)
            )
        )

        status = getattr(review, "status", None)
        rules = getattr(status, "resource_rules", None) if status else None

        print(f"\nNamespace: {ns}")

        if not rules:
            print("  no permissions")
            continue

        rows = build_subject_rows(rules)
        render_subject_table(rows)
