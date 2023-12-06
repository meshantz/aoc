import math
from dataclasses import dataclass

import common


@dataclass
class Race:
    time: int
    best_distance: int


def make_races(parsed: list[common.WholeLine]) -> list[Race]:
    times = [int(i) for i in parsed[0].data.split()[1:]]
    dists = [int(i) for i in parsed[1].data.split()[1:]]

    return [Race(t, d) for t, d in zip(times, dists)]


def make_race(parsed: list[common.WholeLine]) -> Race:
    t = int("".join(parsed[0].data.split()[1:]))
    d = int("".join(parsed[1].data.split()[1:]))

    return Race(t, d)


def race_range(r: Race):
    for t in range(1, r.time):
        if (r.time - t) * t > r.best_distance:
            return r.time - 2 * t + 1
    return 0


def part1(data: list[Race]):
    return math.prod(race_range(race) for race in data)


def part2(data: Race):
    return race_range(data)


def solution():
    raw_data = common.load("data/2023/day06.txt")
    formatted_data1 = make_races(common.parse(raw_data, common.WholeLine))
    formatted_data2 = make_race(common.parse(raw_data, common.WholeLine))

    answer1 = part1(formatted_data1)
    print(f"Part 1: {answer1}")

    answer2 = part2(formatted_data2)
    print(f"Part 2: {answer2}")


def test():
    test1 = """Time:      7  15   30
Distance:  9  40  200"""
    answer1 = part1(make_races(common.parse(test1, common.WholeLine)))
    print(f"Part 1: {answer1}")
    assert answer1 == 288

    test2 = test1
    answer2 = part2(make_race(common.parse(test2, common.WholeLine)))
    print(f"Part 2: {answer2}")
    assert answer2 == 71503
