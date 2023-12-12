import enum
import typing as t
from dataclasses import dataclass

import common


class State(enum.StrEnum):
    WORKING = "."
    BROKEN = "#"
    UNKNOWN = "?"


class Evaluation(enum.StrEnum):
    POSSIBLE = "possible"
    IMPOSSIBLE = "impossible"
    UNDETERMINED = "undetermined"


@dataclass
class SpringRow(common.LineConsumer):
    # this is exactly the same as common.WholeLine, so remove it or modify it to suit the problem
    # or see other common.LineConsumer derivatives
    data: list[State]
    checksum: list[int]

    @classmethod
    def from_lines(cls: type[t.Self], data_iter: t.Iterator[str]) -> t.Self:
        line = next(data_iter)
        data, checksum = line.split()

        return cls([State(v) for v in data], [int(v) for v in checksum.split(",")])


@dataclass
class Summary:
    kind: State
    count: int


def summarize(s: SpringRow) -> list[Summary]:
    result = []
    group: list[State] = []
    for d in s.data:
        if group:
            if group[0] == d:
                group.append(d)
            else:
                result.append(Summary(group[0], len(group)))
                group = [d]
        else:
            group.append(d)

    result.append(Summary(group[0], len(group)))
    return result


def partial_evaluate(partial: list[State], checksum: list[int]):
    # consider up to the first question-mark (partial will not contain that, so whole list here)
    if len(partial) < checksum[0]:
        return Evaluation.UNDETERMINED

    partial_sum = [len(broken) for broken in "".join(partial).split(".") if broken]
    print(partial_sum)

    if len(partial_sum) > len(checksum):
        return Evaluation.IMPOSSIBLE

    for i, j in zip(partial_sum, checksum):
        if i != j:
            # TODO: if this is the last value in partial sum and the last value is broken, it's still possible
            # if partial[-1] =
            return Evaluation.IMPOSSIBLE

    return Evaluation.POSSIBLE


def part1(data: list[SpringRow]):
    # for d in data:
    d = data[0]
    print(partial_evaluate([State.BROKEN, State.WORKING, State.WORKING, State.WORKING], [3, 2, 1]))
    return 0


def part2(data: list[SpringRow]):
    return 0


def solution():
    raw_data = common.load("data/2023/day12.txt")
    formatted_data = common.parse(raw_data, SpringRow)

    answer1 = part1(formatted_data)
    print(f"Part 1: {answer1}")

    answer2 = part2(formatted_data)
    print(f"Part 2: {answer2}")


def test():
    test1 = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""
    answer1 = part1(common.parse(test1, SpringRow))
    print(f"Part 1: {answer1}")
    assert answer1 == 21

    test2 = test1
    answer2 = part2(common.parse(test2, SpringRow))
    print(f"Part 2: {answer2}")
    # assert answer2 == ???
