def pods_to_dict(pods):
    list_of_dicts = []
    for pod in pods:
        dict_of_pod = {}
        dict_of_pod["name"] = pod.metadata.name
        dict_of_pod["namespace"] = pod.metadata.namespace
        dict_of_pod["status"] = pod.status.phase
        list_of_dicts.append(dict_of_pod)
    return list_of_dicts
