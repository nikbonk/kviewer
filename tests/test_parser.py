from src.configParser import parse_config


def test_clusters_table(capsys):
    parse_config("tests/fixtures/kubeconfig.yaml")
    output = capsys.readouterr().out

    assert "dev-cluster" in output
    assert "staging-cluster" in output
    assert "prod-cluster" in output

    assert "https://10.0.0.10:6443" in output
    assert "https://10.0.1.10:6443" in output
    assert "https://10.0.2.10:6443" in output


def test_cluster_count(capsys):
    parse_config("tests/fixtures/kubeconfig.yaml")
    output = capsys.readouterr().out
    assert output.count("-cluster") == 3
