from __future__ import annotations
import typing as t
from dataclasses import dataclass
from dataclasses import field
import operator
import functools

import common


@dataclass
class BridgeCalibrator(common.LineConsumer):
    # this is exactly the same as common.WholeLine, so remove it or modify it to suit the problem
    # or see other common.LineConsumer derivatives
    value: int
    operands: list[int]

    @classmethod
    def from_lines(cls: type[t.Self], data_iter: t.Iterator[str]) -> t.Self:
        line = next(data_iter)
        value, *operands = line.split()
        return cls(int(value.strip(":")), [int(o) for o in operands])


@dataclass
class Node:
    val: t.Callable[[int, int], int] | None
    children: list[Node] = field(default_factory=list)


def cat(left: int, right: int) -> int:
    return int(str(left) + str(right))


def add_mul_add(node: Node, depth: int):
    if depth == 0:
        return

    node.children.append(Node(operator.mul))
    node.children.append(Node(operator.add))

    for child in node.children:
        add_mul_add(child, depth - 1)


def add_mul_add_cat(node: Node, depth: int):
    if depth == 0:
        return

    node.children.append(Node(operator.mul))
    node.children.append(Node(operator.add))
    node.children.append(Node(cat))

    for child in node.children:
        add_mul_add_cat(child, depth - 1)


@functools.cache
def make_operator_tree(depth: int):
    root = Node(None)
    add_mul_add(root, depth)
    return root


@functools.cache
def make_tri_operator_tree(depth: int):
    root = Node(None)
    add_mul_add_cat(root, depth)
    return root


def calculate(node: Node, operands: t.Sequence, test: int, index: int = 0, acc: int = 0) -> int:
    if node.val is None:
        # print(operands[index])
        acc = operands[index]
    else:
        # print(node.val)
        # print(operands[index])
        acc = node.val(acc, operands[index])

    if not node.children:
        # print(acc, "==", test)
        return int(acc == test)

    total = 0
    for child in node.children:
        total += calculate(child, operands, test, index + 1, acc)
        if total:
            return total

    return total


def print_node(node: Node, depth: int = 0):
    print(f"{' ' * depth}{node.val}")
    for child in node.children:
        print_node(child, depth + 1)


def part1(data: t.Sequence[BridgeCalibrator]):
    true_tests = []
    for test in data:
        ops = make_operator_tree(len(test.operands) - 1)
        # print_node(ops)
        count = calculate(ops, test.operands, test.value)
        if count:
            true_tests.append(test.value)

    return sum(true_tests)


def part2(data: t.Iterable[BridgeCalibrator]):
    false_tests = []
    true_tests = []

    for test in data:
        ops = make_operator_tree(len(test.operands) - 1)
        count = calculate(ops, test.operands, test.value)
        if count:
            true_tests.append(test.value)
        else:
            false_tests.append(test)

    for test in false_tests:
        ops = make_tri_operator_tree(len(test.operands) - 1)
        count = calculate(ops, test.operands, test.value)
        if count:
            true_tests.append(test.value)

    return sum(true_tests)


def solution():
    raw_data = common.load("data/2024/day07.txt")
    formatted_data = common.parse(raw_data, BridgeCalibrator)

    answer1 = part1(formatted_data)
    print(f"Part 1: {answer1}")

    answer2 = part2(formatted_data)
    print(f"Part 2: {answer2}")


def test():
    test1 = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""
    answer1 = part1(common.parse(test1, BridgeCalibrator))
    print(f"Part 1: {answer1}")
    # assert answer1 == ???

    test2 = test1
    answer2 = part2(common.parse(test2, BridgeCalibrator))
    print(f"Part 2: {answer2}")
    # assert answer2 == ???
