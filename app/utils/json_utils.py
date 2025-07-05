import collections.abc

def deep_merge(d, u):
    """
    Recursively merges two dictionaries, concatenating lists.
    """
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = deep_merge(d.get(k, {}), v)
        elif isinstance(v, list) and isinstance(d.get(k), list):
            d[k].extend(v)
        else:
            d[k] = v
    return d
