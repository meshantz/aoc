from __future__ import annotations

import collections
import itertools
import enum
import typing as t
from dataclasses import dataclass

import common


@dataclass
class Dish(common.LineConsumer):
    data: list[str]

    @classmethod
    def from_lines(cls: type[t.Self], data_iter: t.Iterator[str]) -> t.Self:
        lines = []
        while line := next(data_iter):
            lines.append(line)

        return cls(lines)

    @property
    def transposed(self):
        return ["".join(c) for c in zip(*self.data)]


@dataclass(frozen=True)
class Pos:
    x: int
    y: int

    def __add__(self, other: Pos):
        return Pos(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Pos):
        return Pos(self.x - other.x, self.y - other.y)


@dataclass
class FixedPoints:
    by_col: dict[int, list[int]]
    by_row: dict[int, list[int]]

    @classmethod
    def from_points(cls, points: set[Pos], width: int, height: int):
        by_col = {i: sorted([p.y for p in points if p.x == i]) for i in range(width)}
        by_row = {j: sorted([p.x for p in points if p.y == j]) for j in range(height)}
        return cls(by_col, by_row)


class Direction(enum.Enum):
    NORTH = (0, -1)
    WEST = (-1, 0)
    SOUTH = (0, 1)
    EAST = (1, 0)


BY_COL = {Direction.NORTH, Direction.SOUTH}
BY_ROW = {Direction.EAST, Direction.WEST}


def print_dish(dish: Dish):
    for line in dish.data:
        print(line)


def print_dish_set(fixed: set[Pos], round: set[Pos], width: int, height: int):
    for j in range(height):
        for i in range(width):
            p = Pos(i, j)
            if p in fixed:
                print("#", end="")
            elif p in round:
                print("O", end="")
            else:
                print(".", end="")
        print()
    print()


def roll(dish: Dish):
    result = []
    for line in dish.transposed:
        parts = line.split("#")
        new_line = []
        for section in parts:
            c = collections.Counter(section)
            new_line.append("O" * c.get("O", 0) + "." * c.get(".", 0))
        result.append("#".join(new_line))
    return Dish(Dish(result).transposed)


def make_sets(dish: Dish):
    fixed: set[Pos] = set()
    round: set[Pos] = set()

    for j, line in enumerate(dish.data):
        for i, char in enumerate(line):
            if char == "#":
                fixed.add(Pos(i, j))
            if char == "O":
                round.add(Pos(i, j))

    # add in the borders
    width = len(dish.data[0])
    height = len(dish.data)
    for i in range(width):
        fixed.add(Pos(i, -1))
        fixed.add(Pos(i, height))
    for j in range(height):
        fixed.add(Pos(-1, j))
        fixed.add(Pos(width, j))

    return fixed, round


def roll_round(fixed: FixedPoints, round: set[Pos], dir: Direction, width: int, height: int):
    """Destroys round"""
    if dir in BY_COL:
        working = fixed.by_col
    else:
        working = fixed.by_row

    new: set[Pos] = set()
    buckets: dict[tuple[int, tuple[int, int]], int] = dict()
    while round:
        cur = round.pop()
        if dir in BY_COL:
            search_in, search_for = cur.x, cur.y
        else:
            search_in, search_for = cur.y, cur.x
        for lower, upper in itertools.pairwise(working[search_in]):
            if search_for > lower and search_for < upper:
                index = (search_in, (lower, upper))
                buckets.setdefault(index, 0)
                buckets[index] += 1
                break

    for (row_or_col, (lower, upper)), count in buckets.items():
        for i in range(count):
            match dir:
                case Direction.NORTH:
                    p = Pos(row_or_col, lower + 1 + i)
                case Direction.SOUTH:
                    p = Pos(row_or_col, upper - 1 - i)
                case Direction.WEST:
                    p = Pos(lower + 1 + i, row_or_col)
                case Direction.EAST:
                    p = Pos(upper - 1 - i, row_or_col)
            new.add(p)

    return new


def hash_set(round: set[Pos]):
    # return frozenset(round)
    acc = 0
    for p in round:
        acc += p.x + p.y * 100_000
    return acc


def part1(data: list[Dish]):
    dish = data[0]
    # print_dish(dish)
    rolled = roll(dish)
    print_dish(rolled)
    south = len(rolled.data)
    return sum(row.count("O") * (south - i) for i, row in enumerate(rolled.data))


def part2(data: list[Dish]):
    dish = data[0]
    width = len(dish.data[0])
    height = len(dish.data)
    fixed_set, round = make_sets(dish)
    fixed = FixedPoints.from_points(fixed_set, width, height)

    print_dish_set(fixed_set, round, width, height)

    rolling = round
    track: list[tuple[int, int]] = []
    i = a = 0
    v = 0
    for i in range(1000):
        for d in [Direction.NORTH, Direction.WEST, Direction.SOUTH, Direction.EAST]:
            rolling = roll_round(fixed, rolling, d, width, height)

        print_dish_set(fixed_set, rolling, width, height)

        v = hash_set(rolling)
        a = sum(height - p.y for p in rolling)
        if (v, a) in track:
            print("seen!")
            break
        track.append((v, a))

    print(track)
    loop_start = track.index((v, a))
    print(loop_start)
    print(i)
    loop_length = i - loop_start
    pre_loop = len(track) - loop_length
    print(f"Before loop: {pre_loop}")
    print(f"Loop length: {loop_length}")
    target_loops = 1_000_000_000
    # target_loops = 20
    to_go = target_loops - len(track)
    print("left:", to_go)
    num_loops = to_go // loop_length
    remainder = to_go % loop_length
    print(num_loops)
    print(remainder)
    if remainder == 0:
        remainder = loop_length
        print(f"set remainder to {remainder}")

    return track[pre_loop + remainder - 1][1]


def solution():
    raw_data = common.load("data/2023/day14.txt")
    raw_data += "\n"
    formatted_data = common.parse(raw_data, Dish)

    answer1 = part1(formatted_data)
    print(f"Part 1: {answer1}")

    answer2 = part2(formatted_data)
    print(f"Part 2: {answer2}")


def test():
    test1 = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....

"""
    answer1 = part1(common.parse(test1, Dish))
    print(f"Part 1: {answer1}")
    assert answer1 == 136

    test2 = test1
    answer2 = part2(common.parse(test2, Dish))
    print(f"Part 2: {answer2}")
    # assert answer2 == ???
