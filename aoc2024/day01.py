import typing as t
from collections import Counter
from dataclasses import dataclass

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


def make_lists(data: list[common.WholeLine]) -> tuple[list[int], list[int]]:
    left, right = [], []
    for line in data:
        a, b = line.data.split()
        left.append(int(a))
        right.append(int(b))

    return left, right


def part1(left: list[int], right: list[int]):
    return sum(abs(y - x) for x, y in zip(sorted(left), sorted(right)))


def part2(left: list[int], right: list[int]):
    counter = Counter(right)
    return sum(i * counter[i] for i in left)


def solution():
    raw_data = common.load("data/2024/day01.txt")
    formatted_data = common.parse(raw_data, common.WholeLine)
    left, right = make_lists(formatted_data)

    answer1 = part1(left, right)
    print(f"Part 1: {answer1}")

    answer2 = part2(left, right)
    print(f"Part 2: {answer2}")


def test():
    test1 = """3   4
4   3
2   5
1   3
3   9
3   3
"""
    answer1 = part1(*make_lists(common.parse(test1, common.WholeLine)))
    print(f"Part 1: {answer1}")
    # assert answer1 == ???

    test2 = test1
    answer2 = part2(*make_lists(common.parse(test2, common.WholeLine)))
    print(f"Part 2: {answer2}")
    # assert answer2 == ???
