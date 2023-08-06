from json import dumps
from json import loads


NONE_TYPE = type(None)
STATE_INFO = {"fun", "order", "state"}


def dump_key(key):
    return dumps(key)


def load_key(key):
    return tuple(loads(key))


def path_ref(data, key):
    for p in key[:-1]:
        data = data[p]
    return data


def del_path(data, key):
    # key cant be empty
    assert key
    for p in key[:-1]:
        data = data[p]
    del data[key[-1]]


def path_data(data, key):
    for p in key:
        data = data[p]
    return data


def path_replace(data, key, value):
    # key cant be empty
    assert key
    for p in key[:-1]:
        data = data[p]
    data[key[-1]] = value


def paths(data, include_dunder=False, include_state_info=False, at=None):
    if at is None:
        at = []
    if isinstance(data, (bool, int, float, str, NONE_TYPE)):
        return
    elif isinstance(data, list):
        for index, item in enumerate(data):
            new_at = at.copy()
            new_at.append(index)
            yield tuple(new_at)
            yield from paths(item, include_dunder, include_state_info, new_at)
        return
    elif isinstance(data, dict):
        for key, item in data.items():
            if (
                not include_dunder
                and isinstance(key, str)
                and key.startswith("__")
                and key.endswith("__")
            ):
                continue
            if not include_state_info and key in STATE_INFO:
                continue
            new_at = at.copy()
            new_at.append(key)
            yield tuple(new_at)
            yield from paths(item, include_dunder, include_state_info, new_at)
        return
    raise NotImplementedError()
