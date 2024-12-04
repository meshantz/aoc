from __future__ import annotations

import contextlib
import typing as t
from dataclasses import dataclass
from dataclasses import field

import common


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def __add__(self, other: Coordinate):
        return Coordinate(self.x + other.x, self.y + other.y)

    def __mul__(self, other: int):
        return Coordinate(self.x * other, self.y * other)


@dataclass
class Cell:
    value: str


@dataclass
class Grid:
    grid: dict[Coordinate, Cell] = field(default_factory=dict)

    def add(self, pos: Coordinate, cell: Cell):
        self.grid[pos] = cell

    def get(self, pos: Coordinate) -> Cell | None:
        return self.grid.get(pos)

    def traverse(self):
        yield from self.grid.items()


def unit_directions():
    for j in [-1, 0, 1]:
        for i in [-1, 0, 1]:
            if i == 0 and j == 0:
                continue
            yield Coordinate(i, j)


def diagonals():
    yield Coordinate(1, 1), Coordinate(1, -1)
    yield Coordinate(1, -1), Coordinate(-1, -1)
    yield Coordinate(-1, -1), Coordinate(-1, 1)
    yield Coordinate(-1, 1), Coordinate(1, 1)


def neighbors(pos: Coordinate, include_self: bool = False):
    for c in unit_directions():
        yield pos + c

    if include_self:
        yield pos


def travel(direction: Coordinate, start: Coordinate):
    return start + direction


def matches(grid: Grid, direction: Coordinate, start: Coordinate, target: str):
    gathered = []
    for i, char in enumerate(target):
        examine = grid.get(start + (direction * i))
        if examine and examine.value == char:
            gathered.append(char)
        else:
            break
    return len(gathered) == len(target)


def search(grid: Grid, target: str):
    found = 0
    for pos, _ in grid.traverse():
        for direction in unit_directions():
            if matches(grid, direction, pos, target):
                found += 1
    return found


def xmas(grid: Grid):
    found = 0
    for pos, cell in grid.traverse():
        if cell.value == "A":
            for d1, d2 in diagonals():
                upper1 = grid.get(pos + d1)
                lower1 = grid.get(pos + (d1 * -1))
                upper2 = grid.get(pos + d2)
                lower2 = grid.get(pos + (d2 * -1))
                if (
                    upper1
                    and lower1
                    and upper2
                    and lower2
                    and upper1.value == "M"
                    and lower1.value == "S"
                    and upper2.value == "M"
                    and lower2.value == "S"
                ):
                    found += 1
    return found


@dataclass
class WordSearch(common.LineConsumer):
    """The full data file, with a single list member that contains every line of the file."""

    grid: Grid = field(default_factory=lambda: Grid())

    @classmethod
    def from_lines(cls: type[t.Self], data_iter: t.Iterator[str]) -> t.Self:
        word_search = cls()
        row = 0
        with contextlib.suppress(StopIteration):
            while line := next(data_iter):
                for col, char in enumerate(line):
                    word_search.grid.add(Coordinate(col, row), Cell(char))
                row += 1

        return word_search


def part1(data: WordSearch):
    return search(data.grid, "XMAS")


def part2(data: WordSearch):
    return xmas(data.grid)


def solution():
    raw_data = common.load("data/2024/day04.txt")
    formatted_data = common.parse_all(raw_data, WordSearch)

    answer1 = part1(formatted_data)
    print(f"Part 1: {answer1}")

    answer2 = part2(formatted_data)
    print(f"Part 2: {answer2}")


def test():
    test1 = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""
    answer1 = part1(common.parse_all(test1, WordSearch))
    print(f"Part 1: {answer1}")
    # assert answer1 == 18

    test2 = """.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........
"""
    answer2 = part2(common.parse_all(test2, WordSearch))
    print(f"Part 2: {answer2}")
    # assert answer2 == 9
