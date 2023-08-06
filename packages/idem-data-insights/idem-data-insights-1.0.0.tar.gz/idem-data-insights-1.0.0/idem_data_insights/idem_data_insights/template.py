from copy import deepcopy

from idem_data_insights.idem_data_insights import high
from idem_data_insights.idem_data_insights import low
from idem_data_insights.idem_data_insights import rpath
from idem_data_insights.idem_data_insights.group_format import group_format


@group_format
def state_fun_template_group(high_data):
    template_groups = {}
    for group in high_data:
        group_name = [
            f"{state}X{count}" for state, count in group[high.STATE_COUNT].items()
        ]
        group_name.sort()
        group_name = "-".join(group_name)
        if group_name not in template_groups:
            template_groups[group_name] = []
        group_order = {}
        for state in group[high.STATES]:
            state_name = f"{state['state']}.{state['fun']}"
            if state_name not in group_order:
                group_order[state_name] = []
            group_order[state_name].append(state)
        for _, states in group_order.items():
            states.sort(key=lambda s: s["order"])
        template_groups[group_name].append(group_order)
    return template_groups


def build_templates(templates_groups):
    templates = {}
    for template in templates_groups:
        # find all immutable keys
        grouping = []
        for group in templates_groups[template]:
            count = -1
            for state_key in group:
                for state in group[state_key]:
                    count += 1
                    if len(grouping) == count:
                        grouping.append([])
                    grouping[count].append(state)
        # remove sub keys
        grouping = [high.high(states) for states in grouping]
        grouping_keys = []
        for high_data in grouping:
            mutable = high_data[high.MUTABLE].copy()
            for key in mutable.copy():
                for i in range(-1, len(key) * -1, -1):
                    try:
                        mutable.remove(key[:i])
                    except KeyError:
                        pass
            grouping_keys.append(mutable)
        # link keys
        link_keys = []
        for spot, group in enumerate(grouping_keys):
            for key in group:
                link = {"key": key, "optional": grouping[spot][high.OPTIONAL][key]}
                if not link["optional"]:
                    high_count = 0
                    key_data = None
                    for name, count in grouping[spot][high.PATH_VARIATIONS][key][
                        high.VARIATIONS
                    ].items():
                        if len(count) > high_count:
                            high_count = len(count)
                            key_data = rpath.path_data(
                                grouping[spot][high.STATES][list(count)[0]], key
                            )
                    if (
                        high_count
                        / grouping[spot][high.PATH_VARIATIONS][key][high.COUNT]
                        > 0.5
                    ):
                        link["default"] = key_data
                link_keys.append({spot: [link]})
        # TODO link keys
        static_data = []
        for _, group in templates_groups[template][0].items():
            static_data.extend(group)
        for link in link_keys:
            for static_state_id, static_paths in link.items():
                static_state = static_data[static_state_id]
                for path in static_paths:
                    if path["optional"]:
                        try:
                            rpath.del_path(static_state, path["key"])
                        except (IndexError, KeyError):
                            pass
                    if "default" in path:
                        rpath.path_replace(static_state, path["key"], path["default"])
        templates[template] = {"links": link_keys, "static": static_data}
    return templates


def fill_templates(templates, templates_groups):
    filled_templates = {}
    for group_name, groups in templates_groups.items():
        if group_name not in filled_templates:
            filled_templates[group_name] = []
        for group in groups:
            spot = -1
            template_copy = deepcopy(templates[group_name])
            filled_templates[group_name].append(template_copy)
            del template_copy["static"]
            for state, states in group.items():
                for s in states:
                    spot += 1
                    for link in template_copy["links"]:
                        if spot in link:
                            try:
                                link["data"] = rpath.path_data(s, link[spot][0]["key"])
                            except (KeyError, IndexError):
                                pass
    return filled_templates


def unroll_templates(templates, filled_templates):
    states = []
    for filled_name, filled_template in filled_templates.items():
        template = templates[filled_name]
        for filled in filled_template:
            state = deepcopy(template["static"])
            for link in filled["links"]:
                if "data" in link:
                    data = link["data"]
                    for state_id in link:
                        if not isinstance(state_id, int):
                            continue
                        s = state[state_id]
                        for path in link[state_id]:
                            key = path["key"]
                            ref = rpath.path_ref(s, key)
                            if isinstance(ref, list):
                                # TODO check key ordering
                                if len(ref) == key[-1]:
                                    ref.append(data)
                                else:
                                    ref[key[-1]] = data
                            else:
                                ref[key[-1]] = data

            state = low.low(state)
            states.append(state)
    states = [high.high(s) for s in states]
    return states
