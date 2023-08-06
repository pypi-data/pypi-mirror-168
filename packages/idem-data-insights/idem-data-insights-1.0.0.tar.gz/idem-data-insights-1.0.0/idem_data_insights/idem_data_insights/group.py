from functools import partial

from idem_data_insights.idem_data_insights import build
from idem_data_insights.idem_data_insights import high
from idem_data_insights.idem_data_insights.group_format import group_format


def null_comp(high_data, other_high_data):
    return False


def state_fun_comp(high_data, other_high_data):
    for state in high_data[high.STATE_COUNT]:
        if state in other_high_data[high.STATE_COUNT]:
            return True
    return False


def build_path_comp(path):
    return partial(path_comp, path=path)


def path_comp(high_data, other_high_data, path):
    if path not in high_data[high.PATHS_DATA]:
        return False
    if path not in other_high_data[high.PATHS_DATA]:
        return False
    return bool(
        high_data[high.PATHS_DATA][path].intersection(
            other_high_data[high.PATHS_DATA][path]
        )
    )


@group_format
def split(high_data, comp_fun):
    new_high = []
    for h in high_data:
        low_split = [[s] for s in h[high.STATES]]
        high_split = build.rebuild_sls(low_split)
        high_joins = {i: {i} for i in range(len(high_split))}
        for index, hs in enumerate(high_split):
            for other_index, other_hs in enumerate(high_split[index + 1 :]):
                other_index += index + 1
                if high_joins[index] != high_joins[other_index] and comp_fun(
                    hs, other_hs
                ):
                    high_joins[index].update(high_joins[other_index])
                    high_joins[other_index].update(high_joins[index])
                    for i in high_joins[index]:
                        high_joins[i].update(high_joins[index])

        for i in range(len(high_joins)):
            if i not in high_joins:
                continue
            new_high.extend(
                build.rebuild_sls([h[high.STATES][s] for s in high_joins[i]])
            )
            for dead_join in high_joins[i]:
                del high_joins[dead_join]
    return new_high


# TODO merge
def merge(high_data, comp_fun):
    pass
