from __future__ import annotations
import contextlib
import typing as t
from dataclasses import dataclass
from dataclasses import field
import heapq

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

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)


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

    def at(self, pos: Coordinate):
        if pos.x >= self.size.x or pos.x < 0 or pos.y >= self.size.y or pos.y < 0:
            return None
        return self.values[pos.y][pos.x]


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


def score_trail(start: Coordinate, grid: Grid):
    nines: t.Set[Coordinate] = set()
    visited: dict[Coordinate, int] = {}
    edges: list[tuple[int, int, Coordinate]] = []
    heapq.heappush(edges, (0, 0, start))
    # bail = 4
    while edges:
        # print(edges)
        distance, height, pos = heapq.heappop(edges)
        edge_val = grid.at(pos)
        # print("considering", pos, distance, height, "=", edge_val)
        if edge_val == height:
            # print("visiting", pos)
            visited[pos] = max(distance, visited.get(pos, -1))
            if edge_val == 9:
                # print("END OF TRAIL!")
                nines.add(pos)
            else:
                for neighbor in neighbor_coords(pos):
                    if visited.get(neighbor, -1) < distance + 1:
                        # print("adding", distance + 1, height + 1, neighbor)
                        heapq.heappush(edges, (distance + 1, height + 1, neighbor))
        # if not bail:
        #     break
        # bail -= 1
    return len(nines)


def collect(pos: Coordinate, grid: Grid, so_far: t.Set[Coordinate]) -> t.Set[t.FrozenSet[Coordinate]]:
    pass_on: t.Set[Coordinate] = {pos} | so_far
    height = grid.at(pos)

    if height is None:
        return set()
    if height == 9:
        return {frozenset(pass_on)}

    result = set()
    for n in neighbor_coords(pos):
        if grid.at(n) == height + 1:
            result |= collect(n, grid, pass_on)

    return result


def part1(data: Topography):
    return sum(score_trail(th, data.grid) for th in data.trail_heads)


def part2(data: Topography):
    return sum(len(collect(th, data.grid, set())) for th in data.trail_heads)


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
"""  # has 5, 6, 5, 3, 1, 3, 5, 3, and 5 = 36 and score 81

    use_data = test5
    answer1 = part1(common.parse_all(use_data, Topography))
    print(f"Part 1: {answer1}")
    # assert answer1 == ???

    test6 = """.....0.
..4321.
..5..2.
..6543.
..7..4.
..8765.
..9....
"""  # score 3
    test7 = """..90..9
...1.98
...2..7
6543456
765.987
876....
987....
"""
    test8 = """012345
123456
234567
345678
4.6789
56789.
"""
    use_data = test5
    answer2 = part2(common.parse_all(use_data, Topography))
    print(f"Part 2: {answer2}")
    # assert answer2 == ???
