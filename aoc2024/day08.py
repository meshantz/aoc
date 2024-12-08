from __future__ import annotations
import contextlib
import typing as t
from dataclasses import dataclass
from dataclasses import field
from itertools import combinations

import common


@dataclass
class City(common.LineConsumer):
    """The full data file, with a single list member that contains every line of the file."""

    antennas: dict[str, list[Coordinate]] = field(default_factory=lambda: {})
    extents: Coordinate = field(default_factory=lambda: Coordinate(-1, -1))

    @classmethod
    def from_lines(cls: type[t.Self], data_iter: t.Iterator[str]) -> t.Self:
        cityscape = cls()
        row = 0
        width = 0
        with contextlib.suppress(StopIteration):
            while line := next(data_iter):
                width = len(line)
                for col, char in enumerate(line):
                    if char not in "#.":
                        cityscape.antennas.setdefault(char, []).append(Coordinate(col, row))
                row += 1

        cityscape.extents = Coordinate(width, row)
        return cityscape


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


def inside(pos: Coordinate, extents: Coordinate):
    return pos.x >= 0 and pos.x < extents.x and pos.y >= 0 and pos.y < extents.y


def print_gridlike(gridlike: t.Container[Coordinate], extents: Coordinate):
    for j in range(extents.y):
        for i in range(extents.x):
            if Coordinate(i, j) in gridlike:
                print("#", end="")
            else:
                print(".", end="")
        print()


def part1(data: City):
    antinodes: t.Set[Coordinate] = set()
    for antenna, positions in data.antennas.items():
        # print(f"Antenna: {antenna}")
        for first, second in combinations(positions, 2):
            # print(f"At: {first}, {second}")
            delta = first - second
            if inside(a1 := (second - delta), data.extents):
                antinodes.add(a1)
            if inside(a2 := (first + delta), data.extents):
                antinodes.add(a2)
            # print(f"Anti: {a1}, {a2}")

    return len(antinodes)


def part2(data: City):
    antinodes: t.Set[Coordinate] = set()
    for antenna, positions in data.antennas.items():
        # print(f"Antenna: {antenna}")
        if len(positions) == 1:
            antinodes.add(positions[0])

        for first, second in combinations(positions, 2):
            # print(f"At: {first}, {second}")
            antinodes.add(first)
            antinodes.add(second)
            delta = first - second

            start = second
            while inside(a1 := (start - delta), data.extents):
                antinodes.add(a1)
                start = a1

            start = first
            while inside(a2 := (start + delta), data.extents):
                antinodes.add(a2)
                start = a2

    # print_gridlike(antinodes, extents=data.extents)
    return len(antinodes)


def solution():
    raw_data = common.load("data/2024/day08.txt")
    formatted_data = common.parse_all(raw_data, City)

    answer1 = part1(formatted_data)
    print(f"Part 1: {answer1}")

    answer2 = part2(formatted_data)
    print(f"Part 2: {answer2}")


def test():
    test1 = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""
    test2 = """..........
...#......
..........
....a.....
..........
.....a....
..........
......#...
..........
..........
"""
    test3 = """T....#....
...T......
.T....#...
.........#
..#.......
..........
...#......
..........
....#.....
..........
"""
    answer1 = part1(common.parse_all(test1, City))
    print(f"Part 1: {answer1}")
    # assert answer1 == 14

    test2 = test1
    answer2 = part2(common.parse_all(test2, City))
    print(f"Part 2: {answer2}")
    # assert answer2 == 34
