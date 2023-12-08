import collections
import math
import typing as t
from dataclasses import dataclass

import common


@dataclass(frozen=True)
class Node:
    name: str
    left: str
    right: str

    @classmethod
    def make(cls: t.Type[t.Self], line: str) -> t.Self:
        name, _, leftish, rightish = line.split()
        return cls(
            name,
            leftish.replace("(", "").replace(",", "").strip(),
            rightish.replace(")", "").replace(",", "").strip(),
        )

    def get(self: t.Self, direction: str):
        match direction:
            case "L":
                return self.left
            case "R":
                return self.right
        raise Exception("Invalid direction!")


def directions_iter(directions: str):
    while True:
        yield from directions


def traverse(start: str, ends: set[str], dir_steps: str, nodes: dict[str, Node]) -> int:
    location = start
    directions = directions_iter(dir_steps)
    steps = 0
    while location not in ends:
        steps += 1
        location = nodes[location].get(next(directions))

    return steps


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


def part1(data: list[common.WholeLine]):
    dir_steps = data[0].data
    nodes = [Node.make(line.data) for line in data[2:]]
    nodes = {n.name: n for n in nodes}

    return traverse("AAA", {"ZZZ"}, dir_steps, nodes)


def part2(data: list[common.WholeLine]):
    dir_steps = data[0].data
    nodes = [Node.make(line.data) for line in data[2:]]
    starts = [n.name for n in nodes if n.name.endswith("A")]
    ends = {n.name for n in nodes if n.name.endswith("Z")}
    nodes = {n.name: n for n in nodes}

    factors = [traverse(s, ends, dir_steps, nodes) for s in starts]
    return lcm(factors)


def solution():
    raw_data = common.load("data/2023/day08.txt")
    formatted_data = common.parse(raw_data, common.WholeLine)

    answer1 = part1(formatted_data)
    print(f"Part 1: {answer1}")

    answer2 = part2(formatted_data)
    print(f"Part 2: {answer2}")


def test():
    test1 = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

    test2 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

    answer1 = part1(common.parse(test1, common.WholeLine))
    print(f"Part 1: {answer1}")
    answer2 = part1(common.parse(test2, common.WholeLine))
    print(f"Part 1: {answer2}")
    assert answer1 == 2
    assert answer2 == 6

    test3 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""
    answer3 = part2(common.parse(test3, common.WholeLine))
    print(f"Part 2: {answer3}")
    assert answer3 == 6
