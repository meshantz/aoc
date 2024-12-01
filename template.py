import contextlib
import typing as t
from dataclasses import dataclass
from dataclasses import field

import common


@dataclass
class CustomParseable(common.LineConsumer):
    # this is exactly the same as common.WholeLine, so remove it or modify it to suit the problem
    # or see other common.LineConsumer derivatives
    data: str

    @classmethod
    def from_lines(cls: type[t.Self], data_iter: t.Iterator[str]) -> t.Self:
        line = next(data_iter)
        return cls(line)


@dataclass
class CustomWholeFile(common.LineConsumer):
    """The full data file, with a single list member that contains every line of the file."""

    # for use with common.parse_all

    # this is pretty much the same as common.WholeFile, so remove it or modify it to suit the problem
    # or see other common.LineConsumer derivatives

    lines: list[str] = field(default_factory=list)

    @classmethod
    def from_lines(cls: type[t.Self], data_iter: t.Iterator[str]) -> t.Self:
        # this is implemented overly verbosely to facilitate customization.
        this_file = cls()
        row = 0
        with contextlib.suppress(StopIteration):
            while line := next(data_iter):
                this_file.lines.append(line)
                row += 1

        return this_file


def part1(data: t.Iterable[common.WholeLine]):
    return 0


def part2(data: t.Iterable[common.WholeLine]):
    return 0


def solution():
    raw_data = common.load("data/{year}/day{day:02}.txt")
    # See also `common.pares_all` for more complicated inputs
    formatted_data = common.parse(raw_data, common.WholeLine)

    answer1 = part1(formatted_data)
    print(f"Part 1: {{answer1}}")

    answer2 = part2(formatted_data)
    print(f"Part 2: {{answer2}}")


def test():
    test1 = """paste-here"""
    answer1 = part1(common.parse(test1, common.WholeLine))
    print(f"Part 1: {{answer1}}")
    # assert answer1 == ???

    test2 = """paste-here"""
    answer2 = part2(common.parse(test2, common.WholeLine))
    print(f"Part 2: {{answer2}}")
    # assert answer2 == ???
