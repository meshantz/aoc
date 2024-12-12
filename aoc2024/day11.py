from __future__ import annotations
import typing as t
from dataclasses import dataclass
from collections import Counter

import common


@dataclass
class Stones(common.LineConsumer):
    head: Node
    tail: Node
    count: int
    stones: list[int]

    @classmethod
    def from_lines(cls: type[t.Self], data_iter: t.Iterator[str]) -> t.Self:
        line = next(data_iter)
        head = tail = None
        count = 0
        stones = []
        for stone in line.split():
            val = int(stone)
            stones.append(val)
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
        return cls(head, tail, count, stones)

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


def blink_one(stone: int) -> tuple[int, int | None]:
    if stone == 0:
        return 1, None
    elif len(val_str := str(stone)) % 2 == 0:
        center = len(val_str) // 2
        left = int(val_str[:center])
        right = int(val_str[center:])
        return left, right
    else:
        return stone * 2024, None


def blink(stones: Stones):
    for stone in stones:
        left, right = blink_one(stone.value)
        if right is None:
            stone.value = left
        else:
            n1 = Node(left)
            n2 = Node(right)
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


def part2(data: Stones, target=75):
    # print(data.stones)
    step = 0
    current = dict(Counter(data.stones))
    next_ = {}
    # print(current)
    while step < target:
        for val, count in current.items():
            if not count:
                continue
            left, right = blink_one(val)
            next_.setdefault(left, 0)
            next_[left] += count
            if right is not None:
                next_.setdefault(right, 0)
                next_[right] += count

        current, next_ = next_, current
        next_.clear()
        step += 1
        # print(current)

    return sum(i for i in current.values())


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
