#!/usr/bin/env python3
import pop.hub


def start():
    hub = pop.hub.Hub()
    hub.pop.sub.add(dyne_name="idem_data_insights")
    hub["idem_data_insights"].init.cli()
