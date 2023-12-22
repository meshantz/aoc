from __future__ import annotations

import typing as t
from dataclasses import dataclass

import common

Extents = tuple[int, int, int, int]


@dataclass(frozen=True)
class Pos:
    x: int
    y: int

    def __add__(self, other: Pos):
        return Pos(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Pos):
        return Pos(self.x - other.x, self.y - other.y)


def get_info(data: list[common.WholeLine]):
    rocks: set[Pos] = set()
    start = Pos(-1, 0)
    for j, line in enumerate(data):
        for i, char in enumerate(line.data):
            if char == "S":
                start = Pos(i, j)
            elif char == "#":
                rocks.add(Pos(i, j))
    return start, rocks


DIRECTIONS = [
    Pos(-1, 0),
    Pos(1, 0),
    Pos(0, 1),
    Pos(0, -1),
]


def neighbors(pos: Pos):
    for dir in DIRECTIONS:
        yield pos + dir


def get_extents(start: Pos, points: set[Pos]) -> Extents:
    min_x, min_y, max_x, max_y = start.x, start.y, start.x, start.y
    for p in points:
        min_x = min(p.x, min_x)
        min_y = min(p.y, min_y)
        max_x = max(p.x, max_x)
        max_y = max(p.y, max_y)
    return min_x, min_y, max_x, max_y


def draw(start: Pos, rocks: set[Pos], reachable: set[Pos], width: int, height: int):
    min_x, min_y, max_x, max_y = get_extents(start, reachable)
    for j in range(min_y - 1, max_y + 2):
        for i in range(min_x - 1, max_x + 2):
            p = Pos(i, j)
            pmod = Pos(p.x % width, p.y % height)
            if pmod in rocks:
                print("#", end="")
            elif p in reachable:
                print("O", end="")
            else:
                print(".", end="")
        print()
    print()


def part1(data: list[common.WholeLine], steps: int):
    start, rocks = get_info(data)
    b1: set[Pos] = set()
    b2: set[Pos] = set()
    buffers = [b1, b2]
    read_buffer, write_buffer = 0, 1
    buffers[write_buffer].add(start)

    for _ in range(steps):
        read_buffer = 1 - read_buffer
        write_buffer = 1 - write_buffer
        buffers[write_buffer].clear()

        for pos in buffers[read_buffer]:
            for n in neighbors(pos):
                if n in rocks:
                    continue
                buffers[write_buffer].add(n)

    return len(buffers[write_buffer])


def part2(data: list[common.WholeLine], steps: int):
    width = len(data[0].data)
    height = len(data)
    print(f"{width} x {height}")
    start, rocks = get_info(data)
    b1: set[Pos] = set()
    b2: set[Pos] = set()
    buffers = [b1, b2]
    read_buffer, write_buffer = 0, 1
    buffers[write_buffer].add(start)

    # need to take advantage of the alternating nature of the two buffers...
    # or is it that the "internal grids" repeat? and then you just need to sort out the /, \, /\, \/, <, >sides?

    for _ in range(steps):
        # print(f"step {i}")
        read_buffer = 1 - read_buffer
        write_buffer = 1 - write_buffer
        buffers[write_buffer].clear()

        for pos in buffers[read_buffer]:
            for n in neighbors(pos):
                nmod = Pos(n.x % width, n.y % height)
                if nmod in rocks:
                    # print(f"X {n} hit a rock")
                    continue
                # print(f"-> {n}")
                buffers[write_buffer].add(n)

        # print()
        draw(start, rocks, buffers[write_buffer], width, height)
    return len(buffers[write_buffer])


def solution():
    raw_data = common.load("data/2023/day21.txt")
    formatted_data = common.parse(raw_data, common.WholeLine)

    answer1 = part1(formatted_data, 64)
    print(f"Part 1: {answer1}")

    answer2 = part2(formatted_data, 80)
    # answer2 = part2(formatted_data, 26501365)
    print(f"Part 2: {answer2}")


def test():
    test1 = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""
    answer1 = part1(common.parse(test1, common.WholeLine), 6)
    print(f"Part 1: {answer1}")
    assert answer1 == 16

    test2 = test1
    answer21 = part2(common.parse(test2, common.WholeLine), 6)
    print(f"Part 2: {answer21}")
    answer22 = part2(common.parse(test2, common.WholeLine), 10)
    print(f"Part 2: {answer22}")
    answer23 = part2(common.parse(test2, common.WholeLine), 40)
    print(f"Part 2: {answer23}")

    # assert answer21 == 16
    # assert answer22 == 50
