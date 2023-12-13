import itertools
import typing as t
from dataclasses import dataclass

import common


@dataclass
class Pattern(common.LineConsumer):
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


def print_side_by_side(l1: list[str], l2: list[str]):
    for i, j in itertools.zip_longest(l1, l2):
        print(f"{i or '': <20}   {j or '': <20}")
    print()


def find_reflection(pattern: list[str]):
    from_stack = list(pattern)  # don't mess with the original list
    to_stack: list[str] = []
    seam = 0

    while from_stack:
        seam += 1
        to_stack.insert(0, from_stack.pop(0))
        # print_side_by_side(from_stack, to_stack)
        if all(a == b for a, b in zip(from_stack, to_stack)):
            break

    if seam != len(pattern):
        # print(f"Seam at {seam}")
        return seam

    # print("No seam")
    return False


def find_smudgy_reflection(pattern: list[str]):
    from_stack = list(pattern)  # don't mess with the original list
    to_stack: list[str] = []
    seam = 0

    while from_stack:
        seam += 1
        to_stack.insert(0, from_stack.pop(0))
        # print_side_by_side(from_stack, to_stack)
        # any one row has exactly 1 difference
        diffs: list[int] = []
        for a, b in zip(from_stack, to_stack):
            diffs.append(sum(c1 != c2 for c1, c2 in zip(a, b)))
        if sum(diffs) == 1:
            break

    if seam != len(pattern):
        # print(f"Seam at {seam}")
        return seam

    # print("No seam")
    return False


def part1(data: list[Pattern]):
    horizontals: list[int] = []
    verticals: list[int] = []

    for d in data:
        if (seam := find_reflection(d.data)) is not False:
            horizontals.append(seam)
        elif (seam := find_reflection(d.transposed)) is not False:
            verticals.append(seam)

    # print(horizontals, verticals)
    return sum(horizontals) * 100 + sum(verticals)


def part2(data: list[Pattern]):
    horizontals: list[int] = []
    verticals: list[int] = []

    for d in data:
        if (seam := find_smudgy_reflection(d.data)) is not False:
            horizontals.append(seam)
        elif (seam := find_smudgy_reflection(d.transposed)) is not False:
            verticals.append(seam)

    # print(horizontals, verticals)
    return sum(horizontals) * 100 + sum(verticals)


def solution():
    raw_data = common.load("data/2023/day13.txt")
    raw_data += "\n"
    formatted_data = common.parse(raw_data, Pattern)

    answer1 = part1(formatted_data)
    print(f"Part 1: {answer1}")

    answer2 = part2(formatted_data)
    print(f"Part 2: {answer2}")


def test():
    test1 = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#

"""
    answer1 = part1(common.parse(test1, Pattern))
    print(f"Part 1: {answer1}")
    assert answer1 == 405

    test2 = test1
    answer2 = part2(common.parse(test2, Pattern))
    print(f"Part 2: {answer2}")
    assert answer2 == 400
