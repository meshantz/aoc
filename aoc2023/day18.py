from __future__ import annotations

import enum
import typing as t
from dataclasses import dataclass

import common


Extents = tuple[int, int, int, int]


class Direction(enum.StrEnum):
    RIGHT = "R"
    LEFT = "L"
    DOWN = "D"
    UP = "U"


class Edge(enum.StrEnum):
    HORIZONTAL = "═"
    VERTICAL = "║"
    UPPER_LEFT = "╔"
    UPPER_RIGHT = "╗"
    LOWER_LEFT = "╚"
    LOWER_RIGHT = "╝"
    UNKNOWN = "*"


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


@dataclass
class HexInstruction:
    count: int
    direction: Direction

    @classmethod
    def from_hex(cls, code: str):
        assert len(code) == 6
        count = int(code[:5], base=16)
        direction = {
            0: Direction.RIGHT,
            1: Direction.DOWN,
            2: Direction.LEFT,
            3: Direction.UP,
        }[int(code[5:], base=16)]
        return cls(count, direction)


@dataclass
class DigStep(common.LineConsumer):
    direction: Direction
    count: int
    hex_instruction: HexInstruction

    @classmethod
    def from_lines(cls: type[t.Self], data_iter: t.Iterator[str]) -> t.Self:
        line = next(data_iter)
        raw_dir, raw_count, rgb = line.split()
        return cls(Direction(raw_dir), int(raw_count), HexInstruction.from_hex(rgb.strip("()#")))


def get_extents(lagoon: dict[Pos, Edge]) -> Extents:
    min_x = min_y = max_x = max_y = 0
    for p in lagoon:
        min_x = min(p.x, min_x)
        min_y = min(p.y, min_y)
        max_x = max(p.x, max_x)
        max_y = max(p.y, max_y)
    return min_x, min_y, max_x, max_y


def show(trench: dict[Pos, Edge], extents: Extents, lagoon: set[Pos]):
    min_x, min_y, max_x, max_y = extents
    for j in range(min_y, max_y + 1):
        for i in range(min_x, max_x + 1):
            p = Pos(i, j)
            dug = trench.get(p, "#" if p in lagoon else ".")
            print(dug, end="")
        print()
    print()


DIG_VECTORS = {
    Direction.UP: Pos(0, -1),
    Direction.DOWN: Pos(0, 1),
    Direction.LEFT: Pos(-1, 0),
    Direction.RIGHT: Pos(1, 0),
}

DIG_EDGES = {
    Direction.UP: Edge.VERTICAL,
    Direction.DOWN: Edge.VERTICAL,
    Direction.LEFT: Edge.HORIZONTAL,
    Direction.RIGHT: Edge.HORIZONTAL,
}


def adjust(prev: Direction, cur: Direction) -> Edge:
    match prev:
        case Direction.UP:
            match cur:
                case Direction.UP:
                    return Edge.VERTICAL
                case Direction.DOWN:
                    return Edge.VERTICAL
                case Direction.LEFT:
                    return Edge.UPPER_RIGHT
                case Direction.RIGHT:
                    return Edge.UPPER_LEFT
        case Direction.DOWN:
            match cur:
                case Direction.UP:
                    return Edge.VERTICAL
                case Direction.DOWN:
                    return Edge.VERTICAL
                case Direction.LEFT:
                    return Edge.LOWER_RIGHT
                case Direction.RIGHT:
                    return Edge.LOWER_LEFT
        case Direction.LEFT:
            match cur:
                case Direction.UP:
                    return Edge.LOWER_LEFT
                case Direction.DOWN:
                    return Edge.UPPER_LEFT
                case Direction.LEFT:
                    return Edge.HORIZONTAL
                case Direction.RIGHT:
                    return Edge.HORIZONTAL
        case Direction.RIGHT:
            match cur:
                case Direction.UP:
                    return Edge.LOWER_RIGHT
                case Direction.DOWN:
                    return Edge.UPPER_RIGHT
                case Direction.LEFT:
                    return Edge.HORIZONTAL
                case Direction.RIGHT:
                    return Edge.HORIZONTAL


def scan(extents: Extents, map: dict[Pos, Edge]):
    switch = {
        PositionType.O: PositionType.I,
        PositionType.I: PositionType.O,
    }
    min_x, min_y, max_x, max_y = extents

    for j in range(min_y, max_y + 1):
        on_edge = None
        state = PositionType.O
        for i in range(min_x - 1, max_x + 2):
            pos = Pos(i, j)
            edge = map.get(pos)
            if on_edge:
                if edge is None:
                    raise Exception(f"Discontinuous Edge ({i}, {j})???")

                if edge in {Edge.UPPER_RIGHT, Edge.LOWER_RIGHT}:
                    if (on_edge == Edge.LOWER_LEFT and edge == Edge.UPPER_RIGHT) or (
                        on_edge == Edge.UPPER_LEFT and edge == Edge.LOWER_RIGHT
                    ):
                        state = switch[state]
                    on_edge = None

                continue

            if edge and edge == Edge.VERTICAL:
                state = switch[state]
            if edge and edge in {Edge.LOWER_LEFT, Edge.UPPER_LEFT}:
                on_edge = edge
                continue

            if edge is None:
                # print(f"[{i}, {j}]: State is {state}")
                yield state, pos


def part1(plan: list[DigStep]):
    print(plan)

    start = current = Pos(0, 0)
    trench = {current: Edge.UNKNOWN}

    prev = Direction.LEFT
    for step in plan:
        trench[current] = adjust(prev, step.direction)
        for _ in range(step.count):
            current += DIG_VECTORS[step.direction]
            trench[current] = DIG_EDGES[step.direction]
        prev = step.direction

    # final step overwrites the start, so adjust at the end...
    trench[start] = adjust(plan[-1].direction, plan[0].direction)

    print(get_extents(trench))
    lagoon = {pos for kind, pos in scan(get_extents(trench), trench) if kind == PositionType.I}
    show(trench, get_extents(trench), lagoon)

    assert lagoon.isdisjoint(trench)

    return len(trench) + len(lagoon)


def part2(plan: list[DigStep]):
    print(plan)

    start = current = Pos(0, 0)
    trench = {current: Edge.UNKNOWN}

    prev = Direction.LEFT
    # TODO: don't track everything. just count things, and track the edges we need
    # hmm. even that's probably too much...
    for step in plan:
        hex_step = step.hex_instruction
        trench[current] = adjust(prev, hex_step.direction)
        for _ in range(hex_step.count):
            current += DIG_VECTORS[hex_step.direction]
            trench[current] = DIG_EDGES[hex_step.direction]
        prev = hex_step.direction

    # final step overwrites the start, so adjust at the end...
    trench[start] = adjust(plan[-1].direction, plan[0].direction)

    extents = get_extents(trench)
    print(get_extents(trench))
    acc = sum(t == PositionType.I for t in scan(extents, trench))
    # show(trench, get_extents(trench), lagoon)

    # assert lagoon.isdisjoint(trench)

    return len(trench) + acc


def solution():
    raw_data = common.load("data/2023/day18.txt")
    formatted_data = common.parse(raw_data, DigStep)

    answer1 = part1(formatted_data)
    print(f"Part 1: {answer1}")

    answer2 = part2(formatted_data)
    print(f"Part 2: {answer2}")


def test():
    test1 = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""
    answer1 = part1(common.parse(test1, DigStep))
    print(f"Part 1: {answer1}")
    assert answer1 == 62

    test2 = test1
    answer2 = part2(common.parse(test2, DigStep))
    print(f"Part 2: {answer2}")
    # assert answer2 == ???
