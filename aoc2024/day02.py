import typing as t
from collections import Counter
from dataclasses import dataclass

import common


@dataclass
class Report(common.LineConsumer):
    # this is exactly the same as common.WholeLine, so remove it or modify it to suit the problem
    # or see other common.LineConsumer derivatives
    levels: t.List[int]
    deltas: t.List[int]
    direction: t.Literal[-1, 0, 1]
    max_delta: int

    @classmethod
    def from_lines(cls: type[t.Self], data_iter: t.Iterator[str]) -> t.Self:
        line = next(data_iter)
        levels = [int(i) for i in line.split()]
        deltas = []
        max_delta = 0
        direction: t.Literal[-1, 0, 1] | None = None

        for i, lvl in enumerate(levels[:-1]):
            delta = levels[i + 1] - lvl
            if delta > 0 and (direction == 1 or direction is None):
                direction = 1
            elif delta < 0 and (direction == -1 or direction is None):
                direction = -1
            else:
                direction = 0
            max_delta = max(abs(delta), max_delta)

        if direction is None:
            direction = 1

        return cls(levels, deltas, direction, max_delta)


def dumb_guard(v: int) -> t.TypeGuard[t.Literal[-1, 0, 1]]:
    return v in {1, -1, 0}


@dataclass
class ReportWithDampener(common.LineConsumer):
    # this is exactly the same as common.WholeLine, so remove it or modify it to suit the problem
    # or see other common.LineConsumer derivatives
    levels: t.List[int]
    deltas: t.List[int]
    direction: t.Literal[-1, 0, 1]
    max_delta: int

    @classmethod
    def from_lines(cls: type[t.Self], data_iter: t.Iterator[str]) -> t.Self:
        line = next(data_iter)
        levels = [int(i) for i in line.split()]
        deltas = []
        max_delta = 0
        dampener_used = False
        directions: list[t.Literal[-1, 0, 1]] = []

        for i, lvl in enumerate(levels[:-1]):
            delta = levels[i + 1] - lvl
            if delta == 0:
                direction = 0
            else:
                direction = int(delta / abs(delta))
            assert dumb_guard(direction)
            directions.append(direction)
            if delta < 1 and delta > 3 and not dampener_used:
                delta = 1
                dampener_used = True
            max_delta = max(abs(delta), max_delta)

        dir_counts = Counter(directions)
        asc = dir_counts[1]
        dsc = dir_counts[-1]
        prevailing_direction = -1 if dsc > asc else 1

        faults = 0
        for direction in directions:
            if direction == 0 or direction != prevailing_direction:
                faults += 1

        if faults > int(dampener_used):
            direction = 0
        else:
            # print(faults, dampener_used)
            direction = prevailing_direction

        return cls(levels, deltas, direction, max_delta)


def part1(reports: t.Iterable[Report]):
    valid = [r for r in reports if r.direction != 0 and r.max_delta <= 3]
    return len(valid)


def part2(reports: t.Iterable[ReportWithDampener]):
    valid = [r for r in reports if r.direction != 0 and r.max_delta <= 3]
    return len(valid)


def solution():
    raw_data = common.load("data/2024/day02.txt")
    # See also `common.pares_all` for more complicated inputs
    formatted_data = common.parse(raw_data, Report)

    answer1 = part1(formatted_data)
    print(f"Part 1: {answer1}")

    formatted_data = common.parse(raw_data, ReportWithDampener)

    answer2 = part2(formatted_data)
    print(f"Part 2: {answer2}")


def test():
    test1 = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""
    answer1 = part1(common.parse(test1, Report))
    print(f"Part 1: {answer1}")
    # assert answer1 == ???

    test2 = test1
    answer2 = part2(common.parse(test2, ReportWithDampener))
    print(f"Part 2: {answer2}")
    # assert answer2 == ???