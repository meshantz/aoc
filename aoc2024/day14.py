from __future__ import annotations
import math
import typing as t
from dataclasses import dataclass

import common


@dataclass
class Robot(common.LineConsumer):
    position: Coordinate
    velocity: Coordinate

    @classmethod
    def from_lines(cls: type[t.Self], data_iter: t.Iterator[str]) -> t.Self:
        line = next(data_iter)
        pos, vel = line.split()
        return cls(parse_assignment("p=", pos), parse_assignment("v=", vel))


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def __add__(self, other: Coordinate):
        return Coordinate(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Coordinate):
        return Coordinate(self.x - other.x, self.y - other.y)

    def __mul__(self, other: int):
        return Coordinate(self.x * other, self.y * other)

    def __lt__(self, other: Coordinate) -> bool:
        return (self.x, self.y) < (other.x, other.y)

    def __mod__(self, other: Coordinate):
        return Coordinate(self.x % other.x, self.y % other.y)


def parse_assignment(label: str, val) -> Coordinate:
    x, y = val.strip().replace(label, "").split(",")
    return Coordinate(int(x), int(y))


def show_grid(robots: t.Mapping[Coordinate, t.Sequence[Robot]], extents: Coordinate):
    for y in range(extents.y):
        for x in range(extents.x):
            pos = Coordinate(x, y)
            if pos in robots:
                print(len(robots[pos]), end="")
            else:
                print(".", end="")
        print()


def quadrant(pos: Coordinate, extents: Coordinate):
    half_x, half_y = extents.x // 2, extents.y // 2
    if pos.x == half_x or pos.y == half_y:
        return None
    elif pos.x < half_x and pos.y < half_y:
        return 1
    elif pos.x > half_x and pos.y < half_y:
        return 2
    elif pos.x < half_x and pos.y > half_y:
        return 3
    else:
        return 4


def part1(data: t.Iterable[Robot], extents=Coordinate(101, 103), seconds: int = 100):
    current: dict[Coordinate, list[Robot]] = {}
    for r in data:
        current.setdefault(r.position, []).append(r)

    # seconds = 5
    final: dict[Coordinate, list[Robot]] = {}
    for r in data:
        result = (r.position + (r.velocity * seconds)) % extents
        final.setdefault(result, []).append(r)

    show_grid(final, extents)
    # print(quadrant(Coordinate(6, 3), extents))

    quadrant_count = {None: 0, 1: 0, 2: 0, 3: 0, 4: 0}
    for pos, robots in final.items():
        quadrant_count[quadrant(pos, extents)] += len(robots)

    del quadrant_count[None]

    return math.prod(quadrant_count.values())


def part2(data: t.Iterable[Robot], extents=Coordinate(101, 103)):
    return 0


def solution():
    raw_data = common.load("data/2024/day14.txt")
    # See also `common.pares_all` for more complicated inputs
    formatted_data = common.parse(raw_data, Robot)

    answer1 = part1(formatted_data)
    print(f"Part 1: {answer1}")

    answer2 = part2(formatted_data)
    print(f"Part 2: {answer2}")


def test():
    test1 = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""
    test2 = """p=2,4 v=2,-3
"""
    answer1 = part1(common.parse(test1, Robot), extents=Coordinate(11, 7))
    print(f"Part 1: {answer1}")
    # assert answer1 == ???

    test2 = test1
    answer2 = part2(common.parse(test2, Robot), extents=Coordinate(11, 7))
    print(f"Part 2: {answer2}")
    # assert answer2 == ???
