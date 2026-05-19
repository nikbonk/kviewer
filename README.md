# kviewer

A Kubernetes companion CLI that provides quick cluster snapshots and useful visibility into cluster states.

`kviewer` is designed for fast day-to-day Kubernetes inspection with cleaner output and better handling of restricted kubeconfigs. Instead of assuming cluster-admin access, it aims to work well with namespace-scoped users and limited RBAC permissions.

## Features

* View pods across one or multiple namespaces
* Respect kubeconfig context defaults
* Support namespace-scoped service accounts and restricted RBAC
* Reduce noisy permission failures
* Clean tabular output
* Modular subcommand structure

---

## Requirements

* Python 3.14+
* A Kubernetes cluster
* A valid kubeconfig
* `uv` installed

---

## Installation

Clone the project:

```bash
git clone git@github.com:nikbonk/kviewer.git
cd kviewer
```

Install dependencies:

```bash
uv sync
```

Run directly:

```bash
uv run kviewer --help
```

Or install as an editable package:

```bash
uv pip install -e .
```

This exposes the CLI entrypoint from:

```toml
[project.scripts]
kviewer = "kviewer.main:main"
```

After installation:

```bash
kviewer --help
```

---

## Usage

List pods using the current kubeconfig context:

```bash
kviewer pods all
```

Specify a kubeconfig:

```bash
kviewer pods all -c ~/tmp/kubeconfig.yaml
```

Specify namespaces:

```bash
kviewer pods all -n default kube-system
```

Example output:

```text
#  Name                               Namespace    Status
--- --------------------------------- ----------- ----------
1   gotenberg-68769c5c67-2xwfq        paperless   Running
2   paperless-cnpg-3                  paperless   Running
```

---

## Restricted kubeconfigs

`kviewer` is intended to work with namespace-scoped service accounts.

For example, if a user only has access to:

* paperless
* monitoring

The CLI should still return available resources rather than fail entirely because inaccessible namespaces exist.

---

## Project layout

```text
kviewer/
├── pyproject.toml
├── README.md
├── src/
│   └── kviewer/
│       ├── main.py
│       ├── pod.py
│       ├── subject.py
│       ├── configParser.py
│       ├── resolve.py
│       └── ...
└── tests/
```

---

## Development

Run locally:

```bash
uv run kviewer
```

Run tests:

```bash
uv run pytest
```

---

## Future ideas

* Deployments
* Services
* Events
* RBAC inspection helpers
* Resource filtering
* Colorized output
