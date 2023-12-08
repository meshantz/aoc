import collections
import math
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


def factorize(val: int) -> list[int]:
    """Expanded prime factors of val as a list. ie 8 => [2, 2, 2]"""
    if val == 1:
        return [val]

    result = []
    n = 2
    cur = val
    limit = val / 2 + 1
    limit = math.sqrt(val) + 1
    while n < limit:
        if cur % n == 0:
            result.append(n)
            cur = cur // n
        else:
            n += 1

    if cur != 1:
        result.append(cur)

    return result


def lcm(factors: list[int]) -> int:
    """Least Common Multiple of all numbers in factors list"""
    all_powers = {}
    for f in factors:
        ff = factorize(f)
        powers = collections.Counter(ff)
        for factor, exponent in powers.items():
            val = max(all_powers.setdefault(factor, 0), exponent)
            all_powers[factor] = val
    return math.prod(f**e for f, e in all_powers.items())
