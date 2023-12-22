from __future__ import annotations

import math
import typing as t
from dataclasses import dataclass

import common


@dataclass(frozen=True)
class Vector2:
    x: int
    y: int

    def __add__(self, other: Vector2):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector2):
        return Vector2(self.x - other.x, self.y - other.y)

    def intersects(self, other: Vector2):
        return self.x >= other.x and self.x <= other.x and self.y >= other.y and self.y <= other.y


@dataclass(frozen=True)
class Vector3:
    x: int
    y: int
    z: int

    def __add__(self, other: Vector3):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vector3):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def horizontal(self):
        return Vector2(self.x, self.y)


@dataclass
class Brick(common.LineConsumer):
    # this is exactly the same as common.WholeLine, so remove it or modify it to suit the problem
    # or see other common.LineConsumer derivatives
    v1: Vector3
    v2: Vector3

    @classmethod
    def from_lines(cls: type[t.Self], data_iter: t.Iterator[str]) -> t.Self:
        line = next(data_iter)
        v1, v2 = line.split("~")
        return cls(
            Vector3(*[int(x) for x in v1.split(",")]),
            Vector3(*[int(x) for x in v2.split(",")]),
        )

    def bottom(self) -> int:
        return min(self.v1.z, self.v2.z)

    def top(self) -> int:
        return max(self.v1.z, self.v2.z)

    def covers(self) -> list[Vector2]:
        """Returns a list of all the points covered by this brick"""
        x1, x2 = sorted([self.v1.x, self.v2.x])
        y1, y2 = sorted([self.v1.y, self.v2.y])

        if self.v1.x == self.v2.x:
            return [Vector2(self.v1.x, y) for y in range(y1, y2 + 1)]
        if self.v1.y == self.v2.y:
            return [Vector2(x, self.v1.y) for x in range(x1, x2 + 1)]
        raise ValueError("Brick has no direction")

    def reposition(self, new_bottom: int) -> Brick:
        """Returns a new brick with the same dimensions but a different bottom"""
        delta = new_bottom - self.bottom()
        return Brick(self.v1 + Vector3(0, 0, delta), self.v2 + Vector3(0, 0, delta))


def has_multiple_directions(brick: Brick):
    d = brick.v1 - brick.v2
    return [d.x != 0, d.y != 0, d.z != 0].count(True) > 1


def get_horizontal_extents(bricks: list[Brick]) -> tuple[int, int, int, int]:
    min_x, min_y, max_x, max_y = math.inf, math.inf, -math.inf, -math.inf
    for brick in bricks:
        unpacked = brick.covers()
        v1 = unpacked[0]
        v2 = unpacked[-1]
        min_x = min(min_x, v1.x, v2.x)
        min_y = min(min_y, v1.y, v2.y)
        max_x = max(max_x, v1.x, v2.x)
        max_y = max(max_y, v1.y, v2.y)
    return int(min_x), int(min_y), int(max_x), int(max_y)


def part1(data: list[Brick]):
    bricks = sorted(data, key=lambda b: (b.bottom(), b.top()))
    min_x, min_y, max_x, max_y = get_horizontal_extents(bricks)
    tops = {Vector2(a, b): 0 for a in range(min_x, max_x + 1) for b in range(min_y, max_y + 1)}
    placed: list[Brick] = []

    print(min_x, min_y, max_x, max_y)
    print(len(tops))
    for brick in bricks:
        can_drop_to = max(tops[point] for point in brick.covers()) + 1
        for point in brick.covers():
            tops[point] = can_drop_to
        placed.append(brick.reposition(can_drop_to))

    for brick in placed:
        print(brick)

    return 0


def part2(data: list[Brick]):
    return 0


def solution():
    raw_data = common.load("data/2023/day22.txt")
    formatted_data = common.parse(raw_data, Brick)

    answer1 = part1(formatted_data)
    print(f"Part 1: {answer1}")

    answer2 = part2(formatted_data)
    print(f"Part 2: {answer2}")


def test():
    test1 = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""
    answer1 = part1(common.parse(test1, Brick))
    print(f"Part 1: {answer1}")
    # assert answer1 == 5

    test2 = test1
    answer2 = part2(common.parse(test2, Brick))
    print(f"Part 2: {answer2}")
    # assert answer2 == ???
