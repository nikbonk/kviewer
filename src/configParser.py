import yaml


def parse_config(config_file):
    clusters = []

    with open(config_file, "r") as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)

    for c in data.get("clusters", []):
        clusters.append([c.get("name"), c.get("cluster", {}).get("server")])

    print("Index".ljust(10) + "Name".ljust(20) + "Server".ljust(30))
    for i, c in enumerate(clusters, start=1):
        print(str(i).ljust(10), end="")
        for col in c:
            print(str(col).ljust(20), end="")
        print()
