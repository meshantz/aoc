import typing as t
from dataclasses import dataclass
from pathlib import Path


class LineConsumer(t.Protocol):
    @classmethod
    def from_lines(cls: t.Type[t.Self], data_iter: t.Iterator[str]) -> t.Self:
        ...


T = t.TypeVar("T", bound=LineConsumer)


@dataclass
class WholeLine(LineConsumer):
    data: str

    @classmethod
    def from_lines(cls: t.Type[t.Self], data_iter: t.Iterator[str]) -> t.Self:
        return cls(next(data_iter))


def parse(raw_data: str, factory: t.Type[T]) -> list[T]:
    lines_iter = iter(raw_data.splitlines())
    parsed = []
    while True:
        try:
            parsed.append(factory.from_lines(lines_iter))
        except StopIteration:
            break

    return parsed


def parse_all(raw_data: str, factory: t.Type[T]) -> T:
    lines_iter = iter(raw_data.splitlines())
    return factory.from_lines(lines_iter)


def load(filename: str | Path) -> str:
    with open(filename) as fp:
        raw = fp.read()
    return raw
