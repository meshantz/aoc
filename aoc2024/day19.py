import contextlib
import typing as t
from dataclasses import dataclass
import functools

import common


@dataclass
class Towels(common.LineConsumer):
    towels: list[str]
    patterns: list[str]

    @classmethod
    def from_lines(cls: type[t.Self], data_iter: t.Iterator[str]) -> t.Self:
        # this is implemented overly verbosely to facilitate customization.

        towels = [t.strip() for t in next(data_iter).split(",")]
        next(data_iter)

        patterns: list[str] = []
        with contextlib.suppress(StopIteration):
            while line := next(data_iter):
                patterns.append(line)

        return cls(towels, patterns)


def part1(data: Towels):
    towels_by_len: dict[int, t.Set[str]] = {}
    for towel in data.towels:
        towels_by_len.setdefault(len(towel), set()).add(towel)

    @functools.cache
    def can_form(pattern: str):
        if pattern in towels_by_len.get(len(pattern), set()):
            return 1

        for size, options in towels_by_len.items():
            head, tail = pattern[:size], pattern[size:]
            if head in options:
                if can_form(tail):
                    return 1
        return 0

    return sum(can_form(p) for p in data.patterns)


def part2(data: Towels):
    towels_by_len: dict[int, t.Set[str]] = {}
    for towel in data.towels:
        towels_by_len.setdefault(len(towel), set()).add(towel)

    @functools.cache
    def can_form(pattern: str):
        total = 0
        for size, options in towels_by_len.items():
            head, tail = pattern[:size], pattern[size:]
            if head in options and head == pattern:
                total += 1
                continue

            # print(f"Breaking up: {head}, {tail}")
            if head in options:
                if head == pattern:
                    # print(f"Done: {pattern}")
                    total += 1
                else:
                    n = can_form(tail)
                    # print(f"Found {n} options for {head}, {tail}")
                    total += n

        return total

    # p = data.patterns[3]
    # return p, can_form(p)
    return sum(can_form(p) for p in data.patterns)


def solution():
    raw_data = common.load("data/2024/day19.txt")
    formatted_data = common.parse_all(raw_data, Towels)

    answer1 = part1(formatted_data)
    print(f"Part 1: {answer1}")

    answer2 = part2(formatted_data)
    print(f"Part 2: {answer2}")


def test():
    test1 = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""
    answer1 = part1(common.parse_all(test1, Towels))
    print(f"Part 1: {answer1}")
    # assert answer1 == ???

    test2 = test1
    answer2 = part2(common.parse_all(test2, Towels))
    print(f"Part 2: {answer2}")
    # assert answer2 == ???
