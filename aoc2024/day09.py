from __future__ import annotations
import contextlib
import typing as t
from dataclasses import dataclass
from dataclasses import field

import common


@dataclass
class Memory(common.LineConsumer):
    files: list[Chunk] = field(default_factory=list)
    free: list[Chunk] = field(default_factory=list)

    @classmethod
    def from_lines(cls: type[t.Self], data_iter: t.Iterator[str]) -> t.Self:
        memory = cls()
        with contextlib.suppress(StopIteration):
            while line := next(data_iter):
                is_file = True
                file_no = 0
                offset = 0
                for char in line:
                    size = int(char)
                    if size != 0:
                        append_list = memory.files if is_file else memory.free
                        new_chunk = Chunk(offset, size, file_no if is_file else None)
                        append_list.append(new_chunk)
                    offset += size
                    file_no += 1 if is_file else 0
                    is_file = not is_file

        return memory


@dataclass
class Chunk:
    start: int
    size: int
    file_no: int | None

    def checksum(self):
        if self.file_no is None:
            return 0
        n0 = self.start
        nn = self.start + self.size - 1
        n = self.size
        # print(n, n0, nn)
        return int((n / 2) * (n0 + nn) * self.file_no)


def shift_left(empty: Chunk, file: Chunk) -> tuple[Chunk, Chunk, Chunk]:
    assert empty.file_no is None
    assert file.file_no is not None

    if empty.size >= file.size:
        filled = Chunk(empty.start, file.size, file.file_no)
        remaining_free = Chunk(empty.start + file.size, empty.size - file.size, None)
        remaining_file = Chunk(0, 0, None)
    else:
        filled = Chunk(empty.start, empty.size, file.file_no)
        remaining_free = Chunk(0, 0, None)
        remaining_file = Chunk(file.start, file.size - empty.size, file.file_no)

    return filled, remaining_free, remaining_file


def part1(data: Memory):
    # print(data)
    # while data.free and data.free[-1].start
    file_list = list(data.files)
    free_list = list(data.free)
    free_list.reverse()
    compacted: list[Chunk] = []
    while True:
        rightmost_file = file_list.pop()
        leftmost_free = free_list.pop()
        # print(rightmost_file, leftmost_free)
        if leftmost_free.start > rightmost_file.start:
            file_list.append(rightmost_file)
            free_list.append(leftmost_free)
            break
        filled, remaining_free, remaining_file = shift_left(leftmost_free, rightmost_file)
        compacted.append(filled)
        if remaining_file.size == 0 and remaining_free.size == 0:
            # print(f"Consumed both entirely")
            pass
        elif remaining_free.size == 0:
            # print(f"Putting {remaining_file} back on the files list")
            file_list.append(remaining_file)
        else:
            # print(f"Putting {remaining_free} back on the free list")
            free_list.append(remaining_free)

    # check = data.files[0]
    # check = compacted[1]
    # print(check, check.checksum())
    # return 0
    # print([c.checksum() for c in compacted], [c.checksum() for c in data.files])
    return sum(c.checksum() for c in compacted) + sum(c.checksum() for c in file_list)


# 8595111142112 too high
# 6400039756455 too low
# 6423258376982
# 15897740276912 way too high :D
# 6396376987752 even lower?
def part2(data: Memory):
    file_list = list(data.files)
    file_list.reverse()
    free_list = list(data.free)
    free_list.sort(key=lambda c: c.start)
    compacted: list[Chunk] = []
    unmoved: list[Chunk] = []
    # print(free_list)

    for file in file_list:
        found = None
        for i, c in enumerate(free_list):
            if c.size >= file.size and c.start < file.start:
                found = i
                break
        if found is None or free_list[found].start > file.start:
            # print(f"Did not move {file}")
            unmoved.append(file)
            continue
        filled, remaining_free, _ = shift_left(free_list[found], file)
        # Don't need to return file to free, do i?
        # print(f"moved {file} to {filled}")
        compacted.append(filled)
        if remaining_free.size == 0:
            free_list = free_list[:found] + free_list[found + 1 :]
        else:
            free_list[found] = remaining_free
            free_list.sort(key=lambda c: c.start)
            # print(f"Returned {remaining_free} to free_list")
            # print(free_list)

    return sum(c.checksum() for c in compacted) + sum(c.checksum() for c in unmoved)


def solution():
    raw_data = common.load("data/2024/day09.txt")
    # See also `common.pares_all` for more complicated inputs
    formatted_data = common.parse_all(raw_data, Memory)

    answer1 = part1(formatted_data)
    print(f"Part 1: {answer1}")

    answer2 = part2(formatted_data)
    print(f"Part 2: {answer2}")


def test():
    test1 = """2333133121414131402
"""
    test2 = """12345
"""
    test_data = test1
    answer1 = part1(common.parse_all(test_data, Memory))
    print(f"Part 1: {answer1}")
    # assert answer1 == ???

    answer2 = part2(common.parse_all(test_data, Memory))
    print(f"Part 2: {answer2}")
    # assert answer2 == ???
