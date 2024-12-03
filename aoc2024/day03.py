import contextlib
import re
import typing as t
from dataclasses import dataclass
from dataclasses import field

import common


RE_MUL = re.compile(r"mul\(\d{1,3},\d{1,3}\)")
RE_MUL_PLUS = re.compile(r"(mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\))")


@dataclass
class Memory(common.LineConsumer):
    """The full data file, with a single list member that contains every line of the file."""

    # for use with common.parse_all

    # this is pretty much the same as common.WholeFile, so remove it or modify it to suit the problem
    # or see other common.LineConsumer derivatives

    program_lines: list[str] = field(default_factory=list)
    program: str = ""

    @classmethod
    def from_lines(cls: type[t.Self], data_iter: t.Iterator[str]) -> t.Self:
        # this is implemented overly verbosely to facilitate customization.
        this_file = cls()
        row = 0
        with contextlib.suppress(StopIteration):
            while line := next(data_iter):
                this_file.program_lines.append(line)
                row += 1

        this_file.program = "\n".join(this_file.program_lines)
        return this_file


@dataclass
class Mul:
    left: int
    right: int

    @classmethod
    def from_str(cls, val: str):
        salient = val[4:-1]
        left, right = salient.split(",")
        return cls(left=int(left), right=int(right))

    def result(self):
        return self.left * self.right


DO = object()
DONT = object()


def make_instructions(inst: t.Iterable[str]):
    result = []
    for i in inst:
        if i.startswith("don't"):
            result.append(DONT)
        elif i.startswith("do"):
            result.append(DO)
        else:
            result.append(Mul.from_str(i))
    return result


def part1(data: Memory):
    vals = [Mul.from_str(v) for v in RE_MUL.findall(data.program)]
    return sum(v.result() for v in vals)


def part2(data: Memory):
    vals = make_instructions(RE_MUL_PLUS.findall(data.program))
    enabled = True
    use = []
    for v in vals:
        if v is DO:
            enabled = True
        elif v is DONT:
            enabled = False
        elif enabled:
            use.append(v)
    return sum(v.result() for v in use)


def solution():
    raw_data = common.load("data/2024/day03.txt")
    # See also `common.pares_all` for more complicated inputs
    formatted_data = common.parse_all(raw_data, Memory)

    answer1 = part1(formatted_data)
    print(f"Part 1: {answer1}")

    answer2 = part2(formatted_data)
    print(f"Part 2: {answer2}")


def test():
    test1 = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""
    answer1 = part1(common.parse_all(test1, Memory))
    print(f"Part 1: {answer1}")
    # assert answer1 == ???

    test2 = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""
    answer2 = part2(common.parse_all(test2, Memory))
    print(f"Part 2: {answer2}")
    # assert answer2 == ???
