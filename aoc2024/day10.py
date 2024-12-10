from __future__ import annotations
import contextlib
import typing as t
from dataclasses import dataclass
from dataclasses import field

import common


@dataclass
class Topography(common.LineConsumer):
    grid: Grid
    trail_heads: list[Coordinate]

    @classmethod
    def from_lines(cls: type[t.Self], data_iter: t.Iterator[str]) -> t.Self:
        # this is implemented overly verbosely to facilitate customization.
        positions: list[list[int | None]] = []
        trail_heads: list[Coordinate] = []
        with contextlib.suppress(StopIteration):
            row_num = 0
            while line := next(data_iter):
                row = []
                for i, c in enumerate(line):
                    if c.isdigit():
                        val = int(c)
                        row.append(val)
                        if val == 0:
                            trail_heads.append(Coordinate(i, row_num))
                    else:
                        row.append(None)

                positions.append(row)
                row_num += 1

        return cls(
            Grid(Coordinate(len(positions), len(positions[0])), positions),
            trail_heads,
        )


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


@dataclass
class Grid:
    size: Coordinate
    values: list[list[int | None]]

    @classmethod
    def empty(cls, size: Coordinate):
        positions = []
        for _ in range(size.y):
            positions.append([None for __ in range(size.x)])
        return cls(size, positions)


def cardinals():
    yield from [
        Coordinate(0, -1),
        Coordinate(1, 0),
        Coordinate(0, 1),
        Coordinate(-1, 0),
    ]


def neighbor_coords(pos: Coordinate, include_self: bool = False):
    for c in cardinals():
        yield pos + c

    if include_self:
        yield pos


def part1(data: Topography):
    print(data)
    return 0


def part2(data: Topography):
    return 0


def solution():
    raw_data = common.load("data/2024/day10.txt")
    # See also `common.pares_all` for more complicated inputs
    formatted_data = common.parse_all(raw_data, Topography)

    answer1 = part1(formatted_data)
    print(f"Part 1: {answer1}")

    answer2 = part2(formatted_data)
    print(f"Part 2: {answer2}")


def test():
    test1 = """0123
1234
8765
9876
"""  # has 1
    test2 = """...0...
...1...
...2...
6543456
7.....7
8.....8
9.....9"""  # has 2
    test3 = """..90..9
...1.98
...2..7
6543456
765.987
876....
987....
"""  # has 4
    test4 = """10..9..
2...8..
3...7..
4567654
...8..3
...9..2
.....01
"""  # has 1 + 2 = 3
    test5 = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""  # has 5, 6, 5, 3, 1, 3, 5, 3, and 5 = 36

    use_data = test5
    answer1 = part1(common.parse_all(use_data, Topography))
    print(f"Part 1: {answer1}")
    # assert answer1 == ???

    answer2 = part2(common.parse_all(use_data, Topography))
    print(f"Part 2: {answer2}")
    # assert answer2 == ???
