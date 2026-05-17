from kubernetes import client

from src.configParser import load_kubeconfig


def setup_subject_args(subparsers, parents=None):
    parse_subject = subparsers.add_parser(
        "subject",
        help="List subjects power",
        parents=parents or [],
    )
    parse_subject.set_defaults(func=get_subject)


def get_subject(args):
    load_kubeconfig(args)
    auth = client.AuthorizationV1Api()
    review = auth.create_self_subject_rules_review(
        body=client.V1SelfSubjectRulesReview(
            spec=client.V1SelfSubjectRulesReviewSpec(),
        ),
    )
    print(review)
