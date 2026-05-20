import json
from pathlib import Path

import yaml
from tabulate import tabulate


def render_cli(data):
    table = tabulate(data["rows"], headers=data["headers"])

    return f"{data['title']}\n{table}\n\n{data['total_label']}: {len(data['rows'])}"


def render_html(data, template_path):
    table_html = tabulate(
        data["rows"],
        headers=data["headers"],
        tablefmt="html",
    )

    template = Path(template_path).read_text(encoding="utf-8")

    return (
        template.replace("{{ title }}", data["title"])
        .replace("{{ table }}", table_html)
        .replace("{{ total }}", f"{data['total_label']}: {len(data['rows'])}")
    )


def render_json(data):
    return json.dumps(data, indent=2)


def render_yaml(data):
    return yaml.dump(data, sort_keys=False)
