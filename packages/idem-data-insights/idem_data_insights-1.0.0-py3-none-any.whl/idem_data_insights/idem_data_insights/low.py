from idem_data_insights.idem_data_insights import okey
from idem_data_insights.idem_data_insights import rpath

INSIGHTS_LOW = "__idem_data_insights_low__"
PATHS = "PATHS"
PATHS_INVERSE = "PATHS_INVERSE"


def low(sls_data):
    for state in sls_data:
        state[INSIGHTS_LOW] = {PATHS: {}, PATHS_INVERSE: {}}
        for path in rpath.paths(state):
            data = okey.object_key(rpath.path_data(state, path))
            state[INSIGHTS_LOW][PATHS][path] = data
            if data not in state[INSIGHTS_LOW][PATHS_INVERSE]:
                state[INSIGHTS_LOW][PATHS_INVERSE][data] = set()
            state[INSIGHTS_LOW][PATHS_INVERSE][data].add(path)
    return sls_data
