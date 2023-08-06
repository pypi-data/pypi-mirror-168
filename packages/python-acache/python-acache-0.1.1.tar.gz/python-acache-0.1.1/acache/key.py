def make_key(*args, **kwargs):
    safe_args = list(make_safe(arg) for arg in args)
    safe_kwargs = list(make_safe(kwargs))
    key = tuple(safe_args + safe_kwargs)

    return hash(key)


def make_safe(args):
    if isinstance(args, dict):
        res = ((k, make_safe(v)) for k, v in args.items())
        res = tuple(sorted(res))
    elif isinstance(args, (list, tuple, set)):
        res = (make_safe(arg) for arg in args)
        res = tuple(sorted(res))
    elif hasattr(args, "__dict__"):
        res = str(vars(args))
    else:
        res = str(args)

    return res
