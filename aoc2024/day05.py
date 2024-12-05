import contextlib
import typing as t
from dataclasses import dataclass
from dataclasses import field

import common


@dataclass
class Rule:
    before: int
    after: int


@dataclass
class Update:
    raw: list[int]
    sorted_: list[int] = field(default_factory=list)

    def center(self):
        return self.sorted_[len(self.sorted_) // 2] if self.sorted_ else 0


@dataclass
class Safety(common.LineConsumer):
    rules: list[Rule] = field(default_factory=list)
    updates: list[Update] = field(default_factory=list)

    @classmethod
    def from_lines(cls: type[t.Self], data_iter: t.Iterator[str]) -> t.Self:
        this_file = cls()

        with contextlib.suppress(StopIteration):
            while line := next(data_iter):
                before, after = line.split("|")
                this_file.rules.append(Rule(int(before), int(after)))

            while line := next(data_iter):
                this_file.updates.append(Update([int(i) for i in line.split(",")]))

        return this_file


def worse_bubble_sort(to_sort: t.Sequence[int], rules: t.Iterable[Rule]) -> list[int]:
    cp = list(to_sort)
    rule_set = {(r.before, r.after) for r in rules}

    for i in range(len(cp) - 1):
        j = i + 1
        while j < len(cp):
            if (cp[j], cp[i]) in rule_set:
                cp[i], cp[j] = cp[j], cp[i]  # swap
                j = i + 1  # need to reset
            else:
                j += 1

    return cp


def part1(data: Safety):
    pre_sorted: list[Update] = []
    for update in data.updates:
        update.sorted_ = worse_bubble_sort(update.raw, data.rules)
        if update.raw == update.sorted_:
            pre_sorted.append(update)

    return sum(p.center() for p in pre_sorted)


def part2(data: Safety):
    unsorted: list[Update] = []
    for update in data.updates:
        update.sorted_ = worse_bubble_sort(update.raw, data.rules)
        if update.raw != update.sorted_:
            unsorted.append(update)

    return sum(u.center() for u in unsorted)


def solution():
    raw_data = common.load("data/2024/day05.txt")
    # See also `common.pares_all` for more complicated inputs
    formatted_data = common.parse_all(raw_data, Safety)

    answer1 = part1(formatted_data)
    print(f"Part 1: {answer1}")

    answer2 = part2(formatted_data)
    print(f"Part 2: {answer2}")


def test():
    test1 = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""
    answer1 = part1(common.parse_all(test1, Safety))
    print(f"Part 1: {answer1}")
    # assert answer1 == 143

    test2 = test1
    answer2 = part2(common.parse_all(test2, Safety))
    print(f"Part 2: {answer2}")
    # assert answer2 == 123
