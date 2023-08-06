from functools import wraps


def group_format(fun):
    @wraps(fun)
    def _group_format_wrapper(high_data, *args, **kwargs):
        if not isinstance(high_data, (list, tuple)):
            high_data = [high_data]
        return fun(high_data, *args, **kwargs)

    return _group_format_wrapper
