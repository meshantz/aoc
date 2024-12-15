from __future__ import annotations
import contextlib
import typing as t
from dataclasses import dataclass
from dataclasses import field

import common


@dataclass
class Warehouse(common.LineConsumer):
    grid: Grid
    robot: Coordinate
    instructions: list[Coordinate]

    @classmethod
    def from_lines(cls: type[t.Self], data_iter: t.Iterator[str]) -> t.Self:
        grid = Grid()
        robot = None
        with contextlib.suppress(StopIteration):
            row_num = 0
            while line := next(data_iter):
                for i, c in enumerate(line):
                    if c in {"#", "O"}:
                        grid.add(Coordinate(i, row_num), c)
                    elif c == "@":
                        robot = Coordinate(i, row_num)

                row_num += 1

        if robot is None:
            raise RuntimeError("Could not find robot in input!")

        istructions: list[Coordinate] = []
        with contextlib.suppress(StopIteration):
            while line := next(data_iter):
                for i in line:
                    istructions.append(cardinals_by_input[i])

        return cls(grid, robot, istructions)


@dataclass
class Grid:
    grid: dict[Coordinate, str] = field(default_factory=dict)

    def clone(self):
        return Grid(self.grid.copy())

    def add(self, pos: Coordinate, cell: str):
        self.grid[pos] = cell

    def remove(self, pos: Coordinate):
        return self.grid.pop(pos, None)

    def at(self, pos: Coordinate) -> str | None:
        return self.grid.get(pos)

    def print(self: Grid, robot: Coordinate):
        size = Coordinate(0, 0)
        for coord in self.grid:
            size = max(size, coord)
        for y in range(size.y + 1):
            for x in range(size.x + 1):
                pos = Coordinate(x, y)
                if pos == robot:
                    print("@", end="")
                    continue
                val = self.at(pos)
                if val:
                    print(val, end="")
                else:
                    print(".", end="")
            print()


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


def cardinals():
    yield from [
        Coordinate(0, -1),
        Coordinate(1, 0),
        Coordinate(0, 1),
        Coordinate(-1, 0),
    ]


cardinal_list = [c for c in cardinals()]
N, W, S, E = cardinal_list
cardinals_by_input = {
    "^": N,
    ">": W,
    "v": S,
    "<": E,
}


def scan_to_empty(start: Coordinate, direction: Coordinate, grid: Grid) -> Coordinate | None:
    """Assumes we'll hit a wall before leaving the search space"""
    current = start
    while consider := (current + direction):
        val = grid.at(consider)
        if val == "#":
            return None
        elif val is None:
            return consider
        current = consider


def part1(data: Warehouse):
    inst_stack = list(reversed(data.instructions))
    grid = data.grid.clone()
    robot = data.robot
    while inst_stack:
        inst = inst_stack.pop()
        try_move = scan_to_empty(robot, inst, grid)
        if try_move is None:
            continue

        move = robot + inst
        if (box := grid.remove(move)) is not None:
            grid.add(try_move, box)
        robot = move

    grid.print(robot)
    return sum(pos.y * 100 + pos.x for pos, val in grid.grid.items() if val == "O")


def part2(data: Warehouse):
    return 0


def solution():
    raw_data = common.load("data/2024/day15.txt")
    # See also `common.pares_all` for more complicated inputs
    formatted_data = common.parse_all(raw_data, Warehouse)

    answer1 = part1(formatted_data)
    print(f"Part 1: {answer1}")

    answer2 = part2(formatted_data)
    print(f"Part 2: {answer2}")


def test():
    test1 = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""
    test2 = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
"""
    test_data = test2
    answer1 = part1(common.parse_all(test_data, Warehouse))
    print(f"Part 1: {answer1}")
    # assert answer1 == ???

    answer2 = part2(common.parse_all(test_data, Warehouse))
    print(f"Part 2: {answer2}")
    # assert answer2 == ???
