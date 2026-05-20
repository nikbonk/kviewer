from pathlib import Path

from .renderer import (
    render_cli,
    render_html,
    render_json,
    render_yaml,
)


def render(data, args):
    fmt = (args.output or "cli").lower()

    if fmt == "html":
        template_path = Path(__file__).parent / "templates" / "report.html"
        content = render_html(data, template_path)

    elif fmt == "json":
        content = render_json(data)

    elif fmt == "yaml":
        content = render_yaml(data)

    else:
        content = render_cli(data)

    # file output
    if getattr(args, "out_file", None):
        with open(args.out_file, "w", encoding="utf-8") as f:
            f.write(content)
        return None

    # CLI output
    print(content)


def build_pod_table(pods):
    rows = [
        [i, p["name"], p["namespace"], p["status"]] for i, p in enumerate(pods, start=1)
    ]

    return {
        "title": "Pods",
        "headers": ["#", "Name", "Namespace", "Status"],
        "rows": rows,
        "total_label": "Total pods",
    }


def build_cluster_table(clusters):
    rows = [[i, name, server] for i, (name, server) in enumerate(clusters, start=1)]

    return {
        "title": "Clusters",
        "headers": ["#", "Name", "Server"],
        "rows": rows,
        "total_label": "Total clusters",
    }
