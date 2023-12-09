import itertools
import typing as t
from dataclasses import dataclass

import common


@dataclass
class History(common.LineConsumer):
    sequence: list[int]

    @classmethod
    def from_lines(cls: type[t.Self], data_iter: t.Iterator[str]) -> t.Self:
        line = next(data_iter)
        return cls([int(i) for i in line.split()])


def derive(sequence: list[int]):
    return [b - a for a, b in itertools.pairwise(sequence)]


def part1(data: list[History]):
    # print(data)

    collect: list[int] = []

    for history in data:
        top = [history.sequence]
        while any(latest := top[-1]):
            top.append(derive(latest))

        for i, seq in enumerate(reversed(top[:-1]), start=1):
            # print(seq, top[-i], seq[-1], top[-i][-1])
            final = seq[-1] + top[-i][-1]
            seq.append(final)

        collect.append(top[0][-1])

    # print(collect)
    return sum(collect)


def part2(data: list[History]):
    collect: list[int] = []

    for history in data:
        top = [history.sequence]
        while any(latest := top[-1]):
            top.append(derive(latest))

        for i, seq in enumerate(reversed(top[:-1]), start=1):
            # print(seq, top[-i], seq[-1], top[-i][-1])
            final = seq[0] - top[-i][0]
            seq.insert(0, final)

        collect.append(top[0][0])

    # print(collect)
    return sum(collect)


def solution():
    raw_data = common.load("data/2023/day09.txt")
    formatted_data = common.parse(raw_data, History)

    answer1 = part1(formatted_data)
    print(f"Part 1: {answer1}")

    answer2 = part2(formatted_data)
    print(f"Part 2: {answer2}")


def test():
    test1 = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""
    answer1 = part1(common.parse(test1, History))
    print(f"Part 1: {answer1}")
    assert answer1 == 114

    test2 = test1
    answer2 = part2(common.parse(test2, History))
    print(f"Part 2: {answer2}")
    assert answer2 == 2
