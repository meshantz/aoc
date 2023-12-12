from __future__ import annotations

import contextlib
import enum
import typing as t
from dataclasses import dataclass

import common


class Compass(enum.StrEnum):
    N = "NORTH"
    S = "SOUTH"
    E = "EAST"
    W = "WEST"


class PositionType(enum.StrEnum):
    I = "IN"
    O = "OUT"


@dataclass(frozen=True)
class Pos:
    x: int
    y: int

    def __add__(self, other: Pos):
        return Pos(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Pos):
        return Pos(self.x - other.x, self.y - other.y)


Shape = t.Literal["|", "-", "L", "J", "7", "F"]


@dataclass(frozen=True)
class Pipe:
    shape: Shape
    connections: frozenset[Compass]


legend: dict[Shape, frozenset[Compass]] = {
    "|": frozenset([Compass.N, Compass.S]),
    "-": frozenset([Compass.E, Compass.W]),
    "L": frozenset([Compass.N, Compass.E]),
    "J": frozenset([Compass.N, Compass.W]),
    "7": frozenset([Compass.S, Compass.W]),
    "F": frozenset([Compass.S, Compass.E]),
}

unlegend: dict[frozenset[Compass], Shape] = {
    frozenset([Compass.N, Compass.S]): "|",
    frozenset([Compass.E, Compass.W]): "-",
    frozenset([Compass.N, Compass.E]): "L",
    frozenset([Compass.N, Compass.W]): "J",
    frozenset([Compass.S, Compass.W]): "7",
    frozenset([Compass.S, Compass.E]): "F",
}


def nav_dir(pos: Pos, dir: Compass) -> Pos:
    match dir:
        case Compass.N:
            return Pos(pos.x, pos.y - 1)
        case Compass.S:
            return Pos(pos.x, pos.y + 1)
        case Compass.E:
            return Pos(pos.x + 1, pos.y)
        case Compass.W:
            return Pos(pos.x - 1, pos.y)

    t.assert_never(dir)


def get_from_dir(from_: Pos, to_: Pos) -> Compass:
    """Return the direction you would have come from to go to to_ from from_"""
    v = to_ - from_
    match v.x, v.y:
        case 1, 0:
            return Compass.W
        case -1, 0:
            return Compass.E
        case 0, 1:
            return Compass.N
        case 0, -1:
            return Compass.S
        case _:
            raise ValueError("Positions must be one unit apart")


def nav_pipe(pos: Pos, pipe: Pipe, came_from: Compass):
    d = set(pipe.connections) - {came_from}
    return nav_dir(pos, d.pop())


def opposite(dir: Compass) -> Compass:
    match dir:
        case Compass.N:
            return Compass.S
        case Compass.S:
            return Compass.N
        case Compass.E:
            return Compass.W
        case Compass.W:
            return Compass.E

    t.assert_never(dir)


def connected(p1: Pipe, p2: Pipe) -> bool:
    return not p1.connections.isdisjoint(p2.connections)


def start_neighbours(start_pos: Pos, map: dict[Pos, Pipe]) -> tuple[Pos, Pos, Shape]:
    """Return the positions of the 2 connected neighbours for the starting position"""
    neighbours = []
    neighbour_dir = []
    for dir in Compass:
        with contextlib.suppress(KeyError):
            if opposite(dir) in map[(n := nav_dir(start_pos, dir))].connections:
                neighbours.append(n)
                neighbour_dir.append(dir)

    n1, n2 = neighbours
    d1, d2 = neighbour_dir
    s = unlegend[frozenset([d1, d2])]
    return n1, n2, s


def map_from(data: list[common.WholeLine]) -> tuple[Pos, dict[Pos, Pipe]]:
    """Return starting position and map of pipes."""
    map: dict[Pos, Pipe] = {}
    start = Pos(-1, -1)
    for j, line in enumerate(data):
        for i, char in enumerate(line.data):
            if char in legend:
                map[Pos(i, j)] = Pipe(char, legend[char])
            if char == "S":
                start = Pos(i, j)

    return start, map


def get_loop(start, map, a, b):
    visited = {start, a, b}

    from_a, to_a = start, a
    from_b, to_b = start, b

    done = False
    while not done:
        next_a = nav_pipe(to_a, map[to_a], get_from_dir(from_a, to_a))
        next_b = nav_pipe(to_b, map[to_b], get_from_dir(from_b, to_b))

        done = next_a in visited or next_b in visited

        visited.add(next_a)
        visited.add(next_b)

        from_a, to_a = to_a, next_a
        from_b, to_b = to_b, next_b
    return visited


def get_extents(points: list[Pos]) -> tuple[int, int, int, int]:
    min_x = min(p.x for p in points)
    min_y = min(p.y for p in points)
    max_x = max(p.x for p in points)
    max_y = max(p.y for p in points)
    return min_x, min_y, max_x, max_y


def scan(extents: tuple[int, int, int, int], map: dict[Pos, Pipe]):
    switch = {
        PositionType.O: PositionType.I,
        PositionType.I: PositionType.O,
    }
    min_x, min_y, max_x, max_y = extents

    for j in range(min_y, max_y + 1):
        on_edge = None
        state = PositionType.O
        for i in range(min_x - 1, max_x + 2):
            pipe = map.get(Pos(i, j))
            if on_edge:
                if pipe is None:
                    raise Exception(f"Discontinuous Pipe ({i}, {j})???")

                if pipe.shape in {"7", "J"}:
                    if (on_edge == "L" and pipe.shape == "7") or (on_edge == "F" and pipe.shape == "J"):
                        state = switch[state]
                    on_edge = None

                continue

            if pipe and pipe.shape == "|":
                state = switch[state]
            if pipe and pipe.shape in {"L", "F"}:
                on_edge = pipe.shape
                continue

            if pipe is None:
                # print(f"[{i}, {j}]: State is {state}")
                yield state


def part1(data: list[common.WholeLine]):
    start, map = map_from(data)
    a, b, start_shape = start_neighbours(start, map)
    visited = get_loop(start, map, a, b)
    return int(len(visited) / 2)


def part2(data: list[common.WholeLine]):
    start, map = map_from(data)
    a, b, start_shape = start_neighbours(start, map)
    visited = get_loop(start, map, a, b)
    map[start] = Pipe(start_shape, legend[start_shape])
    extents = get_extents(list(visited))
    loop_only_map = {pos: map[pos] for pos in visited}

    count = 0
    for t in scan(extents, loop_only_map):
        if t == PositionType.I:
            count += 1

    return count


def solution():
    raw_data = common.load("data/2023/day10.txt")
    formatted_data = common.parse(raw_data, common.WholeLine)

    answer1 = part1(formatted_data)
    print(f"Part 1: {answer1}")

    answer2 = part2(formatted_data)
    print(f"Part 2: {answer2}")


def test():
    test1 = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""

    test2 = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""

    answer11 = part1(common.parse(test1, common.WholeLine))
    print(f"Part 1 [1]: {answer11}")

    answer12 = part1(common.parse(test2, common.WholeLine))
    print(f"Part 1 [2]: {answer12}")

    assert answer11 == 4
    assert answer12 == 8

    test3 = """..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
........."""

    test4 = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""

    answer21 = part2(common.parse(test3, common.WholeLine))
    print(f"Part 2 [1]: {answer21}")

    answer22 = part2(common.parse(test4, common.WholeLine))
    print(f"Part 2 [1]: {answer22}")

    assert answer21 == 4
    assert answer22 == 8
