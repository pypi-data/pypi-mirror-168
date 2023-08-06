from idem_data_insights.idem_data_insights.low import INSIGHTS_LOW
from idem_data_insights.idem_data_insights.low import PATHS
from idem_data_insights.idem_data_insights.low import PATHS_INVERSE


STATES = "STATES"
STATE_COUNT = "STATE_COUNT"
PATH_STATES = "PATH_STATES"
PATHS_DATA = "PATHS_DATA"
DATA_PATHS = "DATA_PATHS"
OPTIONAL = "OPTIONAL"


PATH_VARIATIONS = "PATH_VARIATIONS"
COUNT = "COUNT"
UNIQUE = "UNIQUE"
AVERAGE = "AVERAGE"
VARIATIONS = "VARIATIONS"

MUTABLE = "MUTABLE"
IMMUTABLE = "IMMUTABLE"

PARENTS = "PARENTS"
CHILDREN = "CHILDREN"


def high(sls_data):
    high_data = {
        STATES: sls_data,
        STATE_COUNT: {},
        PATH_STATES: {},
        PATHS_DATA: {},
        DATA_PATHS: {},
        OPTIONAL: {},
        MUTABLE: set(),
        IMMUTABLE: set(),
        PATH_VARIATIONS: {},
        PARENTS: set(),
        CHILDREN: set(),
    }
    # STATE_COUNT
    for state in sls_data:
        fun_call = f"{state['state']}.{state['fun']}"
        if fun_call not in high_data[STATE_COUNT]:
            high_data[STATE_COUNT][fun_call] = 0
        high_data[STATE_COUNT][fun_call] += 1

    # PATHS_STATES
    for index, state in enumerate(sls_data):
        for path in state[INSIGHTS_LOW][PATHS]:
            if path not in high_data[PATH_STATES]:
                high_data[PATH_STATES][path] = set()
            high_data[PATH_STATES][path].add(index)

    # PATHS DATA
    for state in sls_data:
        for path, data in state[INSIGHTS_LOW][PATHS].items():
            if path not in high_data[PATHS_DATA]:
                high_data[PATHS_DATA][path] = set()
            high_data[PATHS_DATA][path].add(data)

    # DATA PATHS
    for index, state in enumerate(sls_data):
        for data in state[INSIGHTS_LOW][PATHS_INVERSE]:
            if data not in high_data[DATA_PATHS]:
                high_data[DATA_PATHS][data] = set()
            high_data[DATA_PATHS][data].add(index)

    # OPTIONAL
    for path, states in high_data[PATH_STATES].items():
        high_data[OPTIONAL][path] = len(states) != len(sls_data)

    # PATH_VARIATION
    for path in high_data[PATH_STATES]:
        state_set = high_data[PATH_STATES][path]
        variations = {COUNT: len(state_set), VARIATIONS: {}}
        high_data[PATH_VARIATIONS][path] = variations
        for state_id in state_set:
            state_data = sls_data[state_id][INSIGHTS_LOW][PATHS][path]
            if state_data not in variations[VARIATIONS]:
                variations[VARIATIONS][state_data] = set()
            variations[VARIATIONS][state_data].add(state_id)
        variations[UNIQUE] = (len(variations[VARIATIONS]) / variations[COUNT]) * 100
        variations[AVERAGE] = sum(
            len(variations[VARIATIONS][v]) for v in variations[VARIATIONS]
        ) / len(variations[VARIATIONS])

    # MUTABLE
    for path, variations in high_data[PATH_VARIATIONS].items():
        if len(variations[VARIATIONS]) != 1 or high_data[OPTIONAL][path]:
            high_data[MUTABLE].add(path)

    # IMMUTABLE
    for path in high_data[PATH_STATES]:
        if path not in high_data[MUTABLE]:
            high_data[IMMUTABLE].add(path)

    # PARENTS
    for path in high_data[PATH_STATES]:
        if len(path) <= 1:
            continue
        high_data[PARENTS].add(path[:-1])

    # CHILDREN
    for path in high_data[PATH_STATES]:
        if path not in high_data[PARENTS]:
            high_data[CHILDREN].add(path)
    return high_data
