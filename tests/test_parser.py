from src.configParser import parse_kubeconfig


def test_clusters_table():
    clusters = parse_kubeconfig("tests/fixtures/kubeconfig.yaml")

    names = [name for name, _ in clusters]
    servers = [server for _, server in clusters]

    assert "dev-cluster" in names
    assert "staging-cluster" in names
    assert "prod-cluster" in names

    assert "https://10.0.0.10:6443" in servers
    assert "https://10.0.1.10:6443" in servers
    assert "https://10.0.2.10:6443" in servers


def test_cluster_count():
    clusters = parse_kubeconfig("tests/fixtures/kubeconfig.yaml")
    assert len(clusters) == 3
