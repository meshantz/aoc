from __future__ import annotations

import enum
import typing as t
from dataclasses import dataclass

import common


@dataclass(frozen=True)
class Pos:
    x: int
    y: int

    def __add__(self, other: Pos):
        return Pos(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Pos):
        return Pos(self.x - other.x, self.y - other.y)


class Direction(enum.StrEnum):
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"


class Mirror(enum.StrEnum):
    NS_SPLITTER = "|"
    EW_SPLITTER = "-"
    WN_ES = "/"
    WS_EN = "\\"
    NONE = "."


OPPOSITES = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.EAST: Direction.WEST,
    Direction.WEST: Direction.EAST,
}
SPLITTERS = {Mirror.EW_SPLITTER, Mirror.NS_SPLITTER}
HORIZONTAL = {Direction.EAST, Direction.WEST}
DIR_TO_VECTOR = {
    Direction.EAST: Pos(1, 0),
    Direction.NORTH: Pos(0, -1),
    Direction.SOUTH: Pos(0, 1),
    Direction.WEST: Pos(-1, 0),
}


def is_splitter(mirror: Mirror):
    return mirror in SPLITTERS


def traverse(mirror: Mirror, travelling: Direction) -> tuple[Direction] | tuple[Direction, Direction]:
    match mirror:
        case Mirror.NONE:
            return (travelling,)
        case Mirror.NS_SPLITTER:
            match travelling:
                case Direction.NORTH:
                    return (travelling,)
                case Direction.SOUTH:
                    return (travelling,)
                case Direction.EAST:
                    return Direction.NORTH, Direction.SOUTH
                case Direction.WEST:
                    return Direction.NORTH, Direction.SOUTH
        case Mirror.EW_SPLITTER:
            match travelling:
                case Direction.NORTH:
                    return Direction.EAST, Direction.WEST
                case Direction.SOUTH:
                    return Direction.EAST, Direction.WEST
                case Direction.EAST:
                    return (travelling,)
                case Direction.WEST:
                    return (travelling,)
        case Mirror.WN_ES:
            match travelling:
                case Direction.NORTH:  # from the south
                    return (Direction.EAST,)
                case Direction.SOUTH:
                    return (Direction.WEST,)
                case Direction.EAST:  # from the west
                    return (Direction.NORTH,)
                case Direction.WEST:
                    return (Direction.SOUTH,)
        case Mirror.WS_EN:
            match travelling:
                case Direction.NORTH:  # from the south
                    return (Direction.WEST,)
                case Direction.SOUTH:
                    return (Direction.EAST,)
                case Direction.EAST:
                    return (Direction.SOUTH,)
                case Direction.WEST:
                    return (Direction.NORTH,)


def navigate(mirror: Mirror, from_: Direction) -> tuple[Pos] | tuple[Pos, Pos]:
    out = traverse(mirror, from_)
    if len(out) == 2:
        return DIR_TO_VECTOR[out[0]], DIR_TO_VECTOR[out[1]]
    return (DIR_TO_VECTOR[out[0]],)


def make_sparse_map(data: list[common.WholeLine]) -> dict[Pos, Mirror]:
    sparse: dict[Pos, Mirror] = {}
    for j, line in enumerate(data):
        for i, char in enumerate(line.data):
            m = Mirror(char)
            if m is not Mirror.NONE:
                sparse[Pos(i, j)] = m
    return sparse


def show_energized(e: set[Pos], width: int, height: int):
    for j in range(height):
        for i in range(width):
            if Pos(i, j) in e:
                print("#", end="")
            else:
                print(".", end="")
        print()
    print()


def get_energized(
    mirrors: dict[Pos, Mirror],
    width: int,
    height: int,
    final_display: bool = False,
    spos: Pos = Pos(0, 0),
    sdir: Direction = Direction.EAST,
):
    unresolved: list[tuple[Pos, Direction]] = [(spos, sdir)]
    visited: dict[Direction, set[Pos]] = {
        Direction.EAST: set(),
        Direction.WEST: set(),
        Direction.NORTH: set(),
        Direction.SOUTH: set(),
    }

    # step = 0
    # bailout = 1_000
    while unresolved:
        # step += 1
        # if step > bailout:
        #     print("Woops! Bailing out")
        #     break
        pos, heading = unresolved.pop()
        visited[heading].add(pos)

        cur_mirror = mirrors.get(pos, Mirror.NONE)
        result = traverse(cur_mirror, heading)
        # print(f"Traversing {pos} going {heading} => {result}")
        for dir in result:
            travel = DIR_TO_VECTOR[dir]
            next_pos = pos + travel
            is_in_grid = next_pos.x >= 0 and next_pos.x < width and next_pos.y >= 0 and next_pos.y < height
            if not is_in_grid:
                # print(f"X: Throwing away {next_pos} - out of bounds")
                continue
            if next_pos in visited[dir]:
                # print(f"X: Throwing away {next_pos} - already travelled {dir} there")
                continue
            # print(f"-> Adding {next_pos}, {dir} to outstanding")
            unresolved.append((pos + travel, dir))

    energized: set[Pos] = set()
    for v in visited.values():
        energized = energized.union(v)

    if final_display:
        show_energized(energized, width, height)
    return len(energized)


def part1(data: list[common.WholeLine]):
    mirrors = make_sparse_map(data)
    width = len(data[0].data)
    height = len(data)
    return get_energized(mirrors, width, height, final_display=True)


def part2(data: list[common.WholeLine]):
    mirrors = make_sparse_map(data)
    width = len(data[0].data)
    height = len(data)
    acc = 0
    for start in range(0, width):
        acc = max(acc, get_energized(mirrors, width, height, spos=Pos(start, 0), sdir=Direction.SOUTH))
        acc = max(acc, get_energized(mirrors, width, height, spos=Pos(start, height - 1), sdir=Direction.NORTH))
    for start in range(0, height):
        acc = max(acc, get_energized(mirrors, width, height, spos=Pos(0, start), sdir=Direction.EAST))
        acc = max(acc, get_energized(mirrors, width, height, spos=Pos(width - 1, start), sdir=Direction.WEST))
    return acc


def solution():
    raw_data = common.load("data/2023/day16.txt")
    formatted_data = common.parse(raw_data, common.WholeLine)

    answer1 = part1(formatted_data)
    print(f"Part 1: {answer1}")

    answer2 = part2(formatted_data)
    print(f"Part 2: {answer2}")


def test():
    test1 = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""
    answer1 = part1(common.parse(test1, common.WholeLine))
    print(f"Part 1: {answer1}")
    assert answer1 == 46

    test2 = test1
    answer2 = part2(common.parse(test2, common.WholeLine))
    print(f"Part 2: {answer2}")
    assert answer2 == 51
