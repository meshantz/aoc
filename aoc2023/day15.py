import typing as t
from dataclasses import dataclass

import common


def parse(raw: str):
    return raw.splitlines()[0]


def hash_alg(v: int, char: str):
    # note: ord is unicode code point, not technically ascii. but the ascii points overlap
    return ((v + ord(char)) * 17) % 256


def print_non_empty(boxes: dict[int, dict[str, int]]):
    for i, box in boxes.items():
        if box:
            print(i, box)
    print()


def focusing_power(boxes: dict[int, dict[str, int]]):
    acc = 0
    for box_number, box_contents in boxes.items():
        for slot_number, focal_length in enumerate(box_contents.values(), 1):
            acc += (box_number + 1) * slot_number * focal_length
    return acc


def part1(init_seq: str):
    stack = [0]
    for char in init_seq:
        if char == ",":
            stack.append(0)
        else:
            stack.append(hash_alg(stack.pop(), char))
    return sum(stack)


def part2(init_seq: str):
    stack = [0]
    label = []
    boxes = {i: {} for i in range(256)}  # python dicts are sorted by default
    next_is_lens = False
    for char in init_seq:
        if next_is_lens:
            lens = int(char)
            next_is_lens = False
            l = "".join(label)
            boxes[stack[-1]][l] = lens
        elif char == ",":
            stack.pop()  # no need to keep them this time?
            stack.append(0)
            label = []
            # print_non_empty(boxes)
        elif char == "-":
            l = "".join(label)
            if l in boxes[stack[-1]]:
                boxes[stack[-1]].pop(l)
        elif char == "=":
            next_is_lens = True
        else:
            stack.append(hash_alg(stack.pop(), char))
            label.append(char)
    # print_non_empty(boxes)
    return focusing_power(boxes)


def solution():
    raw_data = common.load("data/2023/day15.txt")
    formatted_data = parse(raw_data)

    answer1 = part1(formatted_data)
    print(f"Part 1: {answer1}")

    answer2 = part2(formatted_data)
    print(f"Part 2: {answer2}")


def test():
    test1 = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""
    answer1 = part1(parse(test1))
    print(f"Part 1: {answer1}")
    assert answer1 == 1320

    test2 = test1
    answer2 = part2(parse(test2))
    print(f"Part 2: {answer2}")
    assert answer2 == 145
