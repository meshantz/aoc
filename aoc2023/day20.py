from __future__ import annotations

import collections
import enum
import typing as t
from dataclasses import dataclass
from dataclasses import field

import common


class ModuleKind(enum.StrEnum):
    FLIP_FLOP = r"%"
    CONJUNCTION = r"&"
    BROADCAST = "broadcaster"


@dataclass
class Pulse:
    from_: str
    to: str
    high: bool


class StateHandler(t.Protocol):
    def send(self, in_from: str, in_value: bool, mod: Module) -> list[Pulse]:
        ...


class BroadcastStateHandler(StateHandler):
    def send(self, in_from: str, in_value: bool, mod: Module):
        return [Pulse(mod.name, o, in_value) for o in mod.outputs]


@dataclass
class FlipFlopStateHandler(StateHandler):
    is_on: bool = False

    def send(self, in_from: str, in_value: bool, mod: Module):
        if in_value:
            return []
        self.is_on = not self.is_on
        return [Pulse(mod.name, o, self.is_on) for o in mod.outputs]


@dataclass
class ConjunctionStateHandler(StateHandler):
    memory: dict[str, bool] = field(default_factory=dict)

    def send(self, in_from: str, in_value: bool, mod: Module):
        # print(mod.name, self.memory, end=" -> ")
        self.memory[in_from] = in_value
        # print(self.memory)
        result_high = all(pulse is True for pulse in self.memory.values())
        return [Pulse(mod.name, o, not result_high) for o in mod.outputs]

    def add_input(self, mod: Module):
        self.memory[mod.name] = False


handlers: dict[ModuleKind, t.Type[StateHandler]] = {
    ModuleKind.BROADCAST: BroadcastStateHandler,
    ModuleKind.FLIP_FLOP: FlipFlopStateHandler,
    ModuleKind.CONJUNCTION: ConjunctionStateHandler,
}


@dataclass
class Module(common.LineConsumer):
    # this is exactly the same as common.WholeLine, so remove it or modify it to suit the problem
    # or see other common.LineConsumer derivatives
    name: str
    kind: ModuleKind
    outputs: list[str]
    handler: StateHandler

    @classmethod
    def from_lines(cls: type[t.Self], data_iter: t.Iterator[str]) -> t.Self:
        line = next(data_iter)
        desc, defn = line.split("->")

        if (d := desc.strip()) == "broadcaster":
            name = d
            kind = ModuleKind(d)
        else:
            name = desc[1:].strip()
            kind = ModuleKind(desc[0])
        outputs = [o.strip() for o in defn.strip().split(",")]

        return cls(name, kind, outputs, handlers[kind]())


def hash_modules(modules: list[Module]) -> str:
    return "".join(
        [
            "1" if t.cast(FlipFlopStateHandler, m.handler).is_on else "0"
            for m in modules
            if m.kind == ModuleKind.FLIP_FLOP
        ]
    )


def part1(modules: list[Module]):
    by_name = {m.name: m for m in modules}
    for con in modules:
        if con.kind == ModuleKind.CONJUNCTION:
            for sender in modules:
                if con.name in sender.outputs:
                    t.cast(ConjunctionStateHandler, con.handler).add_input(sender)

    # print(by_name)
    pulses: collections.deque[Pulse] = collections.deque()

    hashes: set[str] = set()
    high_pulses: list[int] = []
    low_pulses: list[int] = []

    run_count = 1000

    while (mod_hash := hash_modules(modules)) not in hashes:
        outputs: dict[str, int] = {}
        print(f"Run {mod_hash}", end=" => ")
        hashes.add(mod_hash)
        high_pulses.append(0)
        low_pulses.append(0)
        # print(by_name)
        pulses.append(Pulse("button", "broadcaster", False))
        while pulses:
            process = pulses.popleft()
            if process.high:
                high_pulses[-1] += 1
            else:
                low_pulses[-1] += 1
            # print(process)
            if (new_from := by_name.get(process.to)) is not None:
                pulses.extend(new_from.handler.send(process.from_, process.high, new_from))
            else:
                outputs.setdefault(process.to, 0)
                outputs[process.to] += 1
        print(high_pulses[-1], low_pulses[-1], outputs)
        if len(high_pulses) >= run_count:
            break

    mult, rem = divmod(run_count, len(high_pulses))
    high_total = sum(high_pulses) * mult + sum(high_pulses[:rem])
    mult, rem = divmod(run_count, len(low_pulses))
    low_total = sum(low_pulses) * mult + sum(low_pulses[:rem])

    return high_total * low_total


def part2(modules: list[Module]):
    by_name = {m.name: m for m in modules}
    for con in modules:
        if con.kind == ModuleKind.CONJUNCTION:
            for sender in modules:
                if con.name in sender.outputs:
                    t.cast(ConjunctionStateHandler, con.handler).add_input(sender)

    # print(by_name)
    pulses: collections.deque[Pulse] = collections.deque()

    hashes: set[str] = set()
    high_pulses: list[int] = []
    low_pulses: list[int] = []

    run_count = 1000

    while (mod_hash := hash_modules(modules)) not in hashes:
        outputs: dict[str, int] = {}
        print(f"Run {mod_hash}", end=" => ")
        hashes.add(mod_hash)
        high_pulses.append(0)
        low_pulses.append(0)
        # print(by_name)
        pulses.append(Pulse("button", "broadcaster", False))
        while pulses:
            process = pulses.popleft()
            if process.high:
                high_pulses[-1] += 1
            else:
                low_pulses[-1] += 1
            # print(process)
            if (new_from := by_name.get(process.to)) is not None:
                pulses.extend(new_from.handler.send(process.from_, process.high, new_from))
            else:
                outputs.setdefault(process.to, 0)
                outputs[process.to] += process.high is False
        print(high_pulses[-1], low_pulses[-1], outputs)
        if outputs.get("rx", 0) == 1:
            # seems unlikely this is going to work. can we start at rx and work our way backwards?
            break

    return len(high_pulses)


def solution():
    raw_data = common.load("data/2023/day20.txt")
    formatted_data = common.parse(raw_data, Module)

    answer1 = part1(formatted_data)
    print(f"Part 1: {answer1}")

    answer2 = part2(formatted_data)
    print(f"Part 2: {answer2}")


def test():
    test1 = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""

    test2 = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""

    answer11 = part1(common.parse(test1, Module))
    print(f"Part 1 [1]: {answer11}")
    answer12 = part1(common.parse(test2, Module))
    print(f"Part 1 [2]: {answer12}")

    answer2 = part2(common.parse(test2, Module))
    print(f"Part 2: {answer2}")
    # assert answer2 == ???

    # assert answer11 == ???
    # assert answer12 == ???
