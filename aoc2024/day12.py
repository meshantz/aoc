from __future__ import annotations
import contextlib
import typing as t
from dataclasses import dataclass
from dataclasses import field

import common


@dataclass
class Farm(common.LineConsumer):
    grid: Grid
    extents: Coordinate

    @classmethod
    def from_lines(cls: type[t.Self], data_iter: t.Iterator[str]) -> t.Self:
        # this is implemented overly verbosely to facilitate customization.
        grid = Grid()
        width = 0
        with contextlib.suppress(StopIteration):
            row_num = 0
            while line := next(data_iter):
                width = len(line)
                for i, c in enumerate(line):
                    grid.add(Coordinate(i, row_num), c)
                row_num += 1

        return cls(grid, Coordinate(width, row_num))


@dataclass
class Grid:
    grid: dict[Coordinate, str] = field(default_factory=dict)

    def add(self, pos: Coordinate, cell: str):
        self.grid[pos] = cell

    def get(self, pos: Coordinate) -> str | None:
        return self.grid.get(pos)


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

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)


def cardinals():
    yield from [
        Coordinate(0, -1),
        Coordinate(1, 0),
        Coordinate(0, 1),
        Coordinate(-1, 0),
    ]


def get_neighbor_coords(pos: Coordinate):
    for direction in cardinals():
        yield pos + direction


def collect(start: Coordinate, available: t.Collection[Coordinate], grid: Grid) -> tuple[t.Set[Coordinate], int, int]:
    our_available = set(available)
    perimeter = 4
    collected = {start}
    border = [start]
    kind = grid.get(start)
    if kind is None:
        raise RuntimeError(f"Farm has an unset kind at {start}")
    # print(kind)
    # print("starting with", collected)

    while border:
        consider = border.pop()
        for option in get_neighbor_coords(consider):
            if option in our_available and grid.get(option) == kind:
                # print("adding", option)
                neighbors = set(get_neighbor_coords(option))
                # print("neighbors of", option, "are", neighbors)
                # print("already have", neighbors & collected)
                perimeter += 4 - 2 * len(neighbors & collected)
                collected.add(option)
                our_available.remove(option)
                border.append(option)
        # print("border is now", border)

    # print(kind, "perimeter", perimeter)
    return collected, len(collected), perimeter


def part1(data: Farm):
    visited = set()
    available = set(data.grid.grid.keys())
    total_price = 0
    while available:
        consider = available.pop()
        collected, area, perimeter = collect(consider, available, data.grid)
        total_price += area * perimeter
        # print(collected)
        visited |= collected
        available -= collected
        # break
    return total_price


def part2(data: Farm):
    return 0


def solution():
    raw_data = common.load("data/2024/day12.txt")
    # See also `common.pares_all` for more complicated inputs
    formatted_data = common.parse_all(raw_data, Farm)

    answer1 = part1(formatted_data)
    print(f"Part 1: {answer1}")

    answer2 = part2(formatted_data)
    print(f"Part 2: {answer2}")


def test():
    test1 = """AAAA
BBCD
BBCC
EEEC
"""  # price 140
    test2 = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
"""  # price 772
    test3 = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""  # price 1930
    test_data = test3
    answer1 = part1(common.parse_all(test_data, Farm))
    print(f"Part 1: {answer1}")
    # assert answer1 == ???

    answer2 = part2(common.parse_all(test_data, Farm))
    print(f"Part 2: {answer2}")
    # assert answer2 == ???
