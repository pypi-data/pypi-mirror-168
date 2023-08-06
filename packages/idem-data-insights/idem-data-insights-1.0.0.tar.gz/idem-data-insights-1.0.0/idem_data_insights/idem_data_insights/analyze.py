from copy import deepcopy
from pprint import pprint

from idem_data_insights.idem_data_insights import high
from idem_data_insights.idem_data_insights import low
from idem_data_insights.idem_data_insights import rpath
from idem_data_insights.idem_data_insights.group_format import group_format


@group_format
def state_count(high_data):
    count_groups = []
    for group in high_data:
        count_group = []
        for state, count in group[high.STATE_COUNT].items():
            count_group.append((state, count))
        count_groups.append(
            sorted(count_group, key=lambda k: (k[1], k[0]), reverse=True)
        )
    return count_groups


def state_count_pp(data):
    for index, group in enumerate(data):
        print(f"#### {index}")
        for state, count in group:
            print(f"{state}, {count}")


def _variation_sort_fun(v):
    return (
        len(v["PATH"]),
        abs(50 - v[high.UNIQUE]),
        abs(0.5 - v[high.AVERAGE] / v[high.COUNT]),
        v[high.COUNT],
    )


@group_format
def variation_sort(high_data, sort_fun=_variation_sort_fun):
    variation_groups = []
    for group in high_data:
        variation_group = []
        for path, path_variation in group[high.PATH_VARIATIONS].items():
            variation_group.append({"PATH": path, **path_variation})
        variation_groups.append(variation_group)
    return [sorted(v_group, key=sort_fun) for v_group in variation_groups]


def variation_sort_pp(data):
    for index, group in enumerate(data):
        print(f"#### {index}")
        for v in group:
            print(
                f"{v['PATH']}, COUNT: {v[high.COUNT]}, UNIQUE: {v[high.UNIQUE]}, AVERAGE: {v[high.AVERAGE]}"
            )


@group_format
def mutable_data(high_data, reverse=False):
    m_data = []
    for group in high_data:
        new_group = []
        group = deepcopy(group)
        for low_state in group[high.STATES]:
            # sorting and reverse avoids crash because of list
            paths = list(low_state[low.INSIGHTS_LOW][low.PATHS])
            paths.sort(reverse=True)
            for path in paths:
                if reverse:
                    if path in group[high.MUTABLE] and path in group[high.CHILDREN]:
                        rpath.del_path(low_state, path)
                else:
                    if path in group[high.IMMUTABLE]:
                        rpath.del_path(low_state, path)
            # remove all dunders
            for key in list(low_state.keys()):
                if isinstance(key, str) and key.startswith("__") and key.endswith("__"):
                    del low_state[key]
                elif key in {"fun", "order", "state"}:
                    del low_state[key]
            new_group.append(low_state)
        m_data.append(new_group)
    return m_data


def mutable_data_pp(data):
    for index, group in enumerate(data):
        print(f"#### {index}")
        for g in group:
            pprint(g)
