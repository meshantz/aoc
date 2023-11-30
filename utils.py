from pathlib import Path


def load(filename: str| Path) -> str:
    with open(filename) as fp:
        raw = fp.read()
    return raw
