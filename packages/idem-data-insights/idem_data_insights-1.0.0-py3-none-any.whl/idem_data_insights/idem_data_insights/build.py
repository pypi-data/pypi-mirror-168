from idem_data_insights.idem_data_insights import high
from idem_data_insights.idem_data_insights import low
from idem_data_insights.idem_data_insights.group_format import group_format


def build(sls_data):
    if len(sls_data) and not isinstance(sls_data[0], (tuple, list)):
        sls_data = [sls_data]
    return [high.high(low.low(s)) for s in sls_data]


@group_format
def rebuild(high_data):
    return build([h[high.STATES] for h in high_data])


@group_format
def rebuild_high(high_data):
    return [high.high(h[high.STATES]) for h in high_data]


def rebuild_sls(sls_data):
    if len(sls_data) and not isinstance(sls_data[0], (tuple, list)):
        sls_data = [sls_data]
    return [high.high(s) for s in sls_data]
