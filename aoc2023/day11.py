from __future__ import annotations

import itertools
from dataclasses import dataclass

import common


@dataclass(frozen=True)
class Pos:
    x: int
    y: int

    def __add__(self, other: Pos):
        return Pos(self.x + other.x, self.y + other.y)


def make_map(data: list[common.WholeLine]):
    m = set()
    for j, line in enumerate(data):
        for i, char in enumerate(line.data):
            if char == "#":
                m.add(Pos(i, j))
    return m


def get_extents(m: set[Pos]):
    min_x = min(p.x for p in m)
    min_y = min(p.y for p in m)
    max_x = max(p.x for p in m)
    max_y = max(p.y for p in m)
    return min_x, min_y, max_x, max_y


def expand(m: set[Pos], expansion=2):
    min_x, min_y, max_x, max_y = get_extents(m)
    sx = set(range(min_x, max_x + 1))
    sy = set(range(min_y, max_y + 1))
    for p in m:
        sx.discard(p.x)
        sy.discard(p.y)

    for i in reversed(sorted(sx)):
        m0 = {Pos(p.x, p.y) if p.x < i else Pos(p.x + expansion - 1, p.y) for p in m}
        m = m0

    for j in reversed(sorted(sy)):
        m0 = {Pos(p.x, p.y) if p.y < j else Pos(p.x, p.y + expansion - 1) for p in m}
        m = m0

    return m


def manhattan_distance(p1: Pos, p2: Pos):
    x1, x2 = sorted([p1.x, p2.x])
    y1, y2 = sorted([p1.y, p2.y])
    return (x2 - x1) + (y2 - y1)


def part1(data: list[common.WholeLine]):
    m = make_map(data)
    m = expand(m)
    return sum(manhattan_distance(p1, p2) for p1, p2 in itertools.combinations(m, 2))


def part2(data: list[common.WholeLine], expansion: int = 1_000_000):
    m = make_map(data)
    m = expand(m, expansion=expansion)
    return sum(manhattan_distance(p1, p2) for p1, p2 in itertools.combinations(m, 2))


def solution():
    raw_data = common.load("data/2023/day11.txt")
    formatted_data = common.parse(raw_data, common.WholeLine)

    answer1 = part1(formatted_data)
    print(f"Part 1: {answer1}")

    answer2 = part2(formatted_data)
    print(f"Part 2: {answer2}")


def test():
    test1 = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

    answer1 = part1(common.parse(test1, common.WholeLine))
    print(f"Part 1: {answer1}")
    assert answer1 == 374

    test2 = test1
    answer21 = part2(common.parse(test2, common.WholeLine), expansion=10)
    print(f"Part 2 [1]: {answer21}")

    answer22 = part2(common.parse(test2, common.WholeLine), expansion=100)
    print(f"Part 2 [2]: {answer22}")

    assert answer21 == 1030
    assert answer22 == 8410
