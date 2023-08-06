import pathlib


def get_refs(hub):
    """
    Determine where the sls sources are
    """
    sls_sources = []
    slses = []
    sls = hub.OPT.idem_data_insights.sls
    path = pathlib.Path(sls)
    if path.is_file():
        ref = str(path.stem if path.suffix == ".sls" else path.name)
        slses.append(ref)
        implied = f"file://{path.parent}"
        if implied not in sls_sources:
            sls_sources.append(implied)
    else:
        slses.append(sls)

    return {"sls_sources": sls_sources, "sls": slses}


async def compile(hub) -> dict:
    """
    Execute the cli routine to validate states
    """
    name = "compile"
    src = hub.idem_data_insights.compiler.get_refs()
    await hub.idem.state.validate(
        name=name,
        sls_sources=src["sls_sources"],
        render="jinja|yaml",
        runtime="serial",
        subs=["states"],
        cache_dir="cachedir",
        sls=src["sls"],
        test=True,
        acct_file=None,
        acct_key=None,
        acct_profile=None,
    )

    errors = hub.idem.RUNS[name]["errors"]
    if errors:
        display = hub.output.nested.display(errors)
        print(display)
        # Return a non-zero error code
        return len(errors)

    ret = {
        "high": hub.idem.RUNS[name]["high"],
        "low": hub.idem.RUNS[name]["low"],
        "meta": hub.idem.RUNS[name]["meta"],
    }
    return ret
