from __future__ import annotations

import enum
import typing as t
from dataclasses import dataclass
from dataclasses import field

import common


class Comparison(enum.StrEnum):
    GT = ">"
    LT = "<"


class Attribute(enum.StrEnum):
    EX_COOL = "x"
    MUSICAL = "m"
    AERODYNAMIC = "a"
    SHINY = "s"


@dataclass
class Rule:
    attribute: Attribute
    comparison: Comparison
    value: int
    destination: str

    @classmethod
    def from_text(cls: type[t.Self], text: str) -> t.Self:
        raw_val, dest = text[2:].split(":")
        return cls(Attribute(text[0]), Comparison(text[1]), int(raw_val), dest)

    def evaluate(self, part: PartSpec):
        v = part.as_dict()[self.attribute]  # KeyError if part isn't fully defined...
        match self.comparison:
            case Comparison.GT:
                return v > self.value
            case Comparison.LT:
                return v < self.value


@dataclass
class Workflow:
    name: str
    rules: list[Rule]
    terminal: str

    @classmethod
    def from_line(cls: type[t.Self], line: str) -> t.Self:
        name, remainder = line.split("{")
        rules = remainder.strip("}").split(",")
        return cls(name, [Rule.from_text(r) for r in rules[:-1]], rules[-1])

    def process(self, part: PartSpec):
        for rule in self.rules:
            if rule.evaluate(part):
                return rule.destination

        return self.terminal


@dataclass
class PartAttr:
    attribute: Attribute
    value: int


@dataclass
class PartSpec:
    attrs: list[PartAttr]
    _dict: dict[Attribute, int] | None = field(default=None, init=False, repr=False)

    @classmethod
    def from_line(cls: type[t.Self], line: str) -> t.Self:
        assignments = line.strip("{}").split(",")
        attrs = []
        for a in assignments:
            attr, val = a.split("=")
            attrs.append(PartAttr(Attribute(attr), int(val)))
        return cls(attrs)

    def as_dict(self):
        if self._dict is None:
            self._dict = {attr.attribute: attr.value for attr in self.attrs}
        return self._dict

    def total(self):
        return sum(attr.value for attr in self.attrs)


def parse(data: list[common.WholeLine]):
    is_workflow = True
    workflows: dict[str, Workflow] = {}
    parts: list[PartSpec] = []
    for line in data:
        if not line.data:
            is_workflow = False
            continue
        if is_workflow:
            w = Workflow.from_line(line.data)
            workflows[w.name] = w
        else:
            parts.append(PartSpec.from_line(line.data))
    return workflows, parts


def part1(data: list[common.WholeLine]):
    workflows, parts = parse(data)

    acc = 0
    for part in parts:
        cur = "in"
        while (dest := workflows[cur].process(part)) not in {"A", "R"}:
            cur = dest
        if dest == "A":
            acc += part.total()

    return acc


def part2(data: list[common.WholeLine]):
    workflows, parts = parse(data)
    print(workflows["in"])
    print(len(workflows))
    print(len([w for w in workflows.values() if w.terminal == "A"]))
    return 0


def solution():
    raw_data = common.load("data/2023/day19.txt")
    formatted_data = common.parse(raw_data, common.WholeLine)

    answer1 = part1(formatted_data)
    print(f"Part 1: {answer1}")

    answer2 = part2(formatted_data)
    print(f"Part 2: {answer2}")


def test():
    test1 = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""
    answer1 = part1(common.parse(test1, common.WholeLine))
    print(f"Part 1: {answer1}")
    assert answer1 == 19114

    test2 = test1
    answer2 = part2(common.parse(test2, common.WholeLine))
    print(f"Part 2: {answer2}")
    # assert answer2 == ???
