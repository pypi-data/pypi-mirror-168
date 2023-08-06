from idem_data_insights.idem_data_insights import build


def __init__(hub):
    # Remember not to start your app in the __init__ function
    # This function should just be used to set up the plugin subsystem
    # The run.py is where your app should usually start
    for dyne in ["idem"]:
        hub.pop.sub.add(dyne_name=dyne)


def cli(hub):
    hub.pop.config.load(["idem_data_insights"], cli="idem_data_insights")
    # Your app's options can now be found under hub.OPT.idem_data_insights
    kwargs = dict(hub.OPT.idem_data_insights)

    # Initialize the asyncio event loop
    hub.pop.loop.create()

    # Start the async code
    coroutine = hub.idem_data_insights.init.run(**kwargs)
    hub.pop.Loop.run_until_complete(coroutine)


async def run(hub, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    # Get sls data
    sls_data = (await hub.idem_data_insights.compiler.compile())["low"]
    # get high sls data
    build.build(sls_data)
    print("Done")
