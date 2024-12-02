import typing as t
import math
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
    return v in {-1, 0, 1}


def make_direction(a: int, b: int) -> t.Literal[-1, 0, 1]:
    delta = b - a
    if delta == 0:
        return 0
    else:
        direction = int(delta / abs(delta))
        assert dumb_guard(direction)
        return direction


def is_valid(report: t.Sequence[int], dampener=False) -> bool:
    directions: list[t.Literal[-1, 0, 1]] = [make_direction(a, b) for a, b in zip(report[:-1], report[1:])]
    dir_counts = Counter(directions)
    asc = dir_counts[1]
    dsc = dir_counts[-1]
    prevailing_direction = -1 if dsc > asc else 1

    for i, (a, b) in enumerate(zip(report[:-1], report[1:])):
        delta = b - a

        # check for no increase or decrease
        if delta == 0 and dampener is False:
            # remove a or b and try again
            return is_valid(list(report[:i]) + list(report[i + 1 :]), True) or is_valid(
                list(report[: i + 1]) + list(report[i + 2 :]), True
            )
        elif delta == 0:
            return False

        # check for correct direction
        if math.copysign(delta, prevailing_direction) != delta and dampener is False:
            # remove a or b and try again
            return is_valid(list(report[:i]) + list(report[i + 1 :]), True) or is_valid(
                list(report[: i + 1]) + list(report[i + 2 :]), True
            )
        elif math.copysign(delta, prevailing_direction) != delta:
            return False

        # check for maximum differnece
        if abs(delta) > 3 and dampener is False:
            # remove a or b and try again
            return is_valid(list(report[:i]) + list(report[i + 1 :]), True) or is_valid(
                list(report[: i + 1]) + list(report[i + 2 :]), True
            )
        elif abs(delta) > 3:
            return False

    return True


def part1(reports: t.Iterable[Report]):
    valid = [r for r in reports if r.direction != 0 and r.max_delta <= 3]
    return len(valid)


def part2(reports: t.Iterable[Report]):
    valid = [r for r in reports if is_valid(r.levels)]
    return len(valid)


def solution():
    raw_data = common.load("data/2024/day02.txt")
    # See also `common.pares_all` for more complicated inputs
    formatted_data = common.parse(raw_data, Report)

    answer1 = part1(formatted_data)
    print(f"Part 1: {answer1}")

    formatted_data = common.parse(raw_data, Report)

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
    answer2 = part2(common.parse(test2, Report))
    print(f"Part 2: {answer2}")
    # assert answer2 == ???
