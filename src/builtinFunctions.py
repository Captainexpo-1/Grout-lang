BUILTIN_FUNCTIONS: dict[str, tuple[str,any]] = {
    "print": (
        "void", 
        lambda *args: print(*args)
    ),
    "input": (
        "string", 
        lambda prompt: input(prompt)
    ),
    "parseNumber": (
        "int", 
        lambda num: int(num) if num.isnumeric() else float(num) if num.replace('.', '', 1).isnumeric() else None
    ),
    "str": (
        "string", 
        lambda s: str(s)
    ),
    "len": (
        "int", 
        lambda l: len(l)
    ),
    "range": (
        "list", 
        lambda *args: list(range(*args))
    ),
}