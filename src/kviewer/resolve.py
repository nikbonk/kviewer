def resolve_namespaces(args, context_info):
    if getattr(args, "namespaces", None):
        return args.namespaces
    if context_info:
        return [context_info["namespace"]]
    return ["default"]
