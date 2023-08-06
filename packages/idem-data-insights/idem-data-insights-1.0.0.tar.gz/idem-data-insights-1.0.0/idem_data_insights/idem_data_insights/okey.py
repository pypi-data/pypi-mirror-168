def object_key(obj: object) -> str:
    return f"{type(obj).__name__}-{obj}"
