import argparse
import shlex

from idem_data_insights.idem_data_insights import analyze
from idem_data_insights.idem_data_insights import group

WIZ_VIEWER = argparse.ArgumentParser(
    description="idem_data_insights - Wiz: A wizard that helps breaking up States."
)

WIZ_VIEWER.add_argument(
    "-q", "--quit", default=False, action="store_true", help="quit wizard"
)

WIZ_VIEWER.add_argument(
    "-s",
    "--select",
    nargs="*",
    help="select states to moodily",
    type=int,
    required=False,
)

WIZ_VIEWER.add_argument(
    "-p", "--picked", default=False, action="store_true", help="show picked salt states"
)

WIZ_VIEWER.add_argument(
    "-c", "--count", default=False, action="store_true", help="show state count"
)

WIZ_VIEWER.add_argument(
    "-m", "--mutable", default=False, action="store_true", help="show mutable"
)

WIZ_VIEWER.add_argument(
    "-v", "--variation", default=False, action="store_true", help="show variation"
)

WIZ_VIEWER.add_argument(
    "-g", "--group", default=False, action="store_true", help="group on states"
)

WIZ_VIEWER.add_argument(
    "-n", "--null_split", default=False, action="store_true", help="split all states"
)

WIZ_VIEWER.add_argument("-w", "--path_split", default=None, help="split on path value")

WIZ_VIEWER.add_argument(
    "-o", "--other", nargs="*", help="select 3rd party state", type=str, required=False
)


def _get_args(command=None):
    if command is None:
        command = input(">>> ")
    command = shlex.split(command)
    try:
        return WIZ_VIEWER.parse_args(command)
    except SystemExit:
        pass


def _get_selected(data, selected, inverse=False):
    if not selected:
        if inverse:
            return []
        return data
    selected_data = []
    for spot, states in data:
        if spot not in selected and inverse:
            selected_data.append(states)
        else:
            selected_data.append(states)
    return selected_data


def wiz_runner(data, selected, command, other):
    command = _get_args(command)
    if command is not None:
        if command.quit:
            return False
        if command.select is not None:
            if not command.select:
                selected.clear()
            else:
                for i in command.select:
                    if i < 0 or i >= len(data):
                        print(f"{repr(i)} is not in range of a salt state.")
                        continue
                    selected.add(i)
        if command.picked:
            if not len(selected):
                print(set(range(len(data))))
            else:
                print(selected)
        if command.count:
            analyze.state_count_pp(analyze.state_count(_get_selected(data, selected)))
        if command.mutable:
            analyze.mutable_data_pp(analyze.mutable_data(_get_selected(data, selected)))
        if command.variation:
            analyze.variation_sort_pp(
                analyze.variation_sort(_get_selected(data, selected))
            )
        if command.group:
            groups = group.split(_get_selected(data, selected), group.state_fun_comp)
            non_groups = _get_selected(data, selected, True)
            data.clear()
            data.extend(groups)
            data.extend(non_groups)
            selected.clear()
        if command.null_split:
            groups = group.split(_get_selected(data, selected), group.null_comp)
            non_groups = _get_selected(data, selected, True)
            data.clear()
            data.extend(groups)
            data.extend(non_groups)
            selected.clear()
        if command.path_split is not None:
            # TODO support path indexing of arrays
            groups = group.split(
                _get_selected(data, selected),
                group.build_path_comp(tuple(command.path_split.split("."))),
            )
            non_groups = _get_selected(data, selected, True)
            data.clear()
            data.extend(groups)
            data.extend(non_groups)
            selected.clear()
        if command.other is not None:
            # TODO handle errors on bad keys or out of index
            other[command.other[0]](command.other(data, selected, *command.other[1:]))
    return True


def wiz(data, other=None):
    if other is None:
        other = {}
    selected = set()
    _get_args("-h")
    while wiz_runner(data, selected, input(">>> "), other):
        pass
    return data
