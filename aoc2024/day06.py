from __future__ import annotations
import contextlib
import typing as t
from dataclasses import dataclass
from dataclasses import field
from itertools import cycle

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
class SecurityGuard(common.LineConsumer):
    """The full data file, with a single list member that contains every line of the file."""

    obstacles: Grid = field(default_factory=lambda: Grid())
    guard_position: Coordinate = field(default_factory=lambda: Coordinate(-1, -1))
    extents: Coordinate = field(default_factory=lambda: Coordinate(-1, -1))

    @classmethod
    def from_lines(cls: type[t.Self], data_iter: t.Iterator[str]) -> t.Self:
        room = cls()
        row = 0
        width = 0
        with contextlib.suppress(StopIteration):
            while line := next(data_iter):
                width = len(line)
                for col, char in enumerate(line):
                    if char == "#":
                        room.obstacles.add(Coordinate(col, row), Cell(char))
                    elif char == "^":
                        room.guard_position = Coordinate(col, row)
                row += 1

        room.extents = Coordinate(width, row)
        return room


@dataclass
class Grid:
    grid: dict[Coordinate, Cell] = field(default_factory=dict)

    def add(self, pos: Coordinate, cell: Cell):
        self.grid[pos] = cell

    def remove(self, pos: Coordinate) -> Cell | None:
        return self.grid.pop(pos, None)

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


def neighbors(pos: Coordinate, include_self: bool = False):
    for c in unit_directions():
        yield pos + c

    if include_self:
        yield pos


def travel(direction: Coordinate, start: Coordinate):
    return start + direction


def leaves(pos: Coordinate, extents: Coordinate):
    return not (pos.x >= 0 and pos.x < extents.x and pos.y >= 0 and pos.y < extents.y)


def try_move(pos: Coordinate, direction: Coordinate, obstacles: Grid):
    new_pos = travel(direction, pos)
    if obstacles.get(new_pos) is None:
        return new_pos


def get_cardinals():
    yield from cycle(
        [
            Coordinate(0, -1),
            Coordinate(1, 0),
            Coordinate(0, 1),
            Coordinate(-1, 0),
        ]
    )


def part1(data: SecurityGuard):
    cardinals = get_cardinals()
    facing = next(cardinals)
    current = data.guard_position
    visit: dict[Coordinate, int] = {}

    while not leaves(current, data.extents):
        visit.setdefault(current, 0)
        visit[current] += 1
        next_pos = try_move(current, facing, data.obstacles)
        i = 0
        while next_pos is None:
            i += 1
            facing = next(cardinals)
            next_pos = try_move(current, facing, data.obstacles)
        if i > 1:
            print(f"Turned: {i}")
        current = next_pos

    return len(visit)


def does_it_loop(
    facing: Coordinate,
    start: Coordinate,
    been_there: t.Mapping[Coordinate, t.Iterable[Coordinate]],
    obstacles: Grid,
    extents: Coordinate,
):
    cardinals = get_cardinals()
    while next(cardinals) != facing:
        pass

    visit: dict[Coordinate, t.Set[Coordinate]] = {}
    for k, v in been_there.items():
        visit[k] = {d for d in v}

    current = start
    while not leaves(current, extents):
        visit.setdefault(current, set()).add(facing)
        next_pos = try_move(current, facing, obstacles)

        while next_pos is None:
            facing = next(cardinals)
            next_pos = try_move(current, facing, obstacles)

        if facing in visit.get(next_pos, set()):
            return True
        current = next_pos

    return False


def part2(data: SecurityGuard):
    cardinals = get_cardinals()
    facing = next(cardinals)

    current = data.guard_position
    visit: dict[Coordinate, t.Set[Coordinate]] = {}
    placeholder = Cell("O")
    loop_obstacle_positions = set()

    while not leaves(current, data.extents):
        visit.setdefault(current, set()).add(facing)
        next_pos = try_move(current, facing, data.obstacles)
        while next_pos is None:
            facing = next(cardinals)
            next_pos = try_move(current, facing, data.obstacles)

        if next_pos != data.guard_position and next_pos not in visit:
            # pretend there's an obstacle here instead.
            data.obstacles.add(next_pos, placeholder)
            if does_it_loop(facing, current, visit, data.obstacles, data.extents):
                loop_obstacle_positions.add(next_pos)
            data.obstacles.remove(next_pos)

        current = next_pos

    return len(loop_obstacle_positions)


def solution():
    raw_data = common.load("data/2024/day06.txt")
    # See also `common.pares_all` for more complicated inputs
    formatted_data = common.parse_all(raw_data, SecurityGuard)

    answer1 = part1(formatted_data)
    print(f"Part 1: {answer1}")

    answer2 = part2(formatted_data)
    print(f"Part 2: {answer2}")


def test():
    test1 = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""
    answer1 = part1(common.parse_all(test1, SecurityGuard))
    print(f"Part 1: {answer1}")
    # assert answer1 == 41

    test2 = test1
    answer2 = part2(common.parse_all(test2, SecurityGuard))
    print(f"Part 2: {answer2}")
    # assert answer2 == ???
