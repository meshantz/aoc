from __future__ import annotations
import contextlib
import typing as t
from dataclasses import dataclass
from dataclasses import field

import common


@dataclass
class Stones(common.LineConsumer):
    head: Node
    tail: Node
    count: int

    @classmethod
    def from_lines(cls: type[t.Self], data_iter: t.Iterator[str]) -> t.Self:
        line = next(data_iter)
        head = tail = None
        count = 0
        for stone in line.split():
            val = int(stone)
            node = Node(val)
            node.left = tail
            if tail:
                tail.right = node
            tail = node
            if head is None:
                head = node
            count += 1

        if head is None or tail is None:
            raise Exception("Unexpected input!")
        return cls(head, tail, count)

    def __iter__(self):
        cur = self.head
        while cur != None:
            original_right = cur.right
            yield cur
            cur = original_right


@dataclass
class Node:
    value: int
    left: Node | None = None
    right: Node | None = None


def blink(stones: Stones):
    for stone in stones:
        if stone.value == 0:
            stone.value = 1
        elif len(val_str := str(stone.value)) % 2 == 0:
            center = len(val_str) // 2
            n1 = Node(int(val_str[:center]))
            n2 = Node(int(val_str[center:]))
            n1.left = stone.left
            n1.right = n2
            n2.left = n1
            n2.right = stone.right
            if stone == stones.head:
                stones.head = n1
            if stone == stones.tail:
                stones.tail = n2
            if stone.left:
                stone.left.right = n1
            if stone.right:
                stone.right.left = n2
            stones.count += 1
        else:
            stone.value *= 2024


def print_stones(s: Stones):
    for stone in s:
        print(stone.value, end=" ")
    print()


def part1(data: Stones):
    print_stones(data)
    for _ in range(25):
        blink(data)
        # print_stones(data)
    return data.count


def part2(data: Stones):
    return 0


def solution():
    raw_data = common.load("data/2024/day11.txt")
    # See also `common.pares_all` for more complicated inputs
    formatted_data = common.parse_all(raw_data, Stones)

    answer1 = part1(formatted_data)
    print(f"Part 1: {answer1}")

    answer2 = part2(formatted_data)
    print(f"Part 2: {answer2}")


def test():
    test1 = """125 17
"""
    answer1 = part1(common.parse_all(test1, Stones))
    print(f"Part 1: {answer1}")
    assert answer1 == 55312

    test2 = test1
    answer2 = part2(common.parse_all(test2, Stones))
    print(f"Part 2: {answer2}")
    # assert answer2 == ???
