import typing as t
from dataclasses import dataclass
import itertools

import common


@dataclass
class Almanac(common.LineConsumer):
    source: str | None
    destination: str
    seeds: list[int] | None = None
    mappings: list[list[int]] | None = None

    @classmethod
    def from_lines(cls: type[t.Self], data_iter: t.Iterator[str]) -> t.Self:
        # FIXME: to make this work, I needed to add a newline to the end of the input file
        lines = []
        while (line := next(data_iter)) != "":
            lines.append(line)

        header, *mappings = lines
        if header.startswith("seeds: "):
            return cls(None, "seed", seeds=[int(x) for x in header.split()[1:]])

        s, _, d = header.split()[0].split("-")
        mapping_list = [[int(m) for m in mapping.split()] for mapping in mappings]
        return cls(source=s, destination=d, mappings=mapping_list)


def find_dest(val: int, a: Almanac) -> int:
    assert a.mappings is not None
    for dest_start, src_start, count in a.mappings:
        if val >= src_start and val < src_start + count:
            offset = val - src_start
            return dest_start + offset
    return val


def find_source(val: int, a: Almanac) -> int:
    assert a.mappings is not None
    for dest_start, src_start, count in a.mappings:
        if val >= dest_start and val < dest_start + count:
            offset = val - dest_start
            return src_start + offset
    return val


def in_next(value: int, source: str, dest_by_source: dict[str, Almanac]):
    dest = dest_by_source[source]
    return find_dest(value, dest), dest.destination


def in_prev(value: int, dest: str, source_by_dest: dict[str, Almanac]):
    source = source_by_dest[dest]
    assert source.source is not None
    return find_source(value, source), source.source


def find_location(dest_by_source: dict[str, Almanac], val: int):
    source = "seed"
    while source != "location":
        # print(f"{source.capitalize()} {val}", end=", ")
        val, source = in_next(val, source, dest_by_source)
    # print(f"{source.capitalize()} {val}")
    return val


def location_has_seed(source_by_dest: dict[str, Almanac], val: int):
    dest = "location"
    while dest != "seed":
        val, dest = in_prev(val, dest, source_by_dest)
    return val


def get_locations(seeds: list[int], dest_by_source: dict[str, Almanac]):
    for val in seeds:
        yield find_location(dest_by_source, val)


def has_seed(seeds: Almanac, seed):
    assert seeds.seeds is not None
    for start, count in itertools.batched(seeds.seeds, 2):
        if seed >= start and seed < start + count:
            return True
    return False


def part1(data: list[Almanac]):
    seeds, *mappings = data
    dest_by_source = {m.source: m for m in mappings if m.source is not None}
    assert seeds.seeds is not None
    return min(get_locations(seeds.seeds, dest_by_source))


def part2(data: list[Almanac]):
    seeds, *mappings = data
    source_by_dest = {m.destination: m for m in mappings if m.source is not None}
    assert seeds.seeds is not None
    location = 0
    bail_out = 993500720
    while True:
        possible_seed = location_has_seed(source_by_dest, location)
        if has_seed(seeds, possible_seed):
            return location
        location += 1
        if location > bail_out:
            raise Exception("Something went wrong, because the first part had a seed here!")


def solution():
    raw_data = common.load("data/2023/day05.txt")
    formatted_data = common.parse(raw_data, Almanac)

    answer1 = part1(formatted_data)
    print(f"Part 1: {answer1}")

    answer2 = part2(formatted_data)
    print(f"Part 2: {answer2}")


def test():
    test1 = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4

"""
    answer1 = part1(common.parse(test1, Almanac))
    print(f"Part 1: {answer1}")
    assert answer1 == 35

    test2 = test1
    answer2 = part2(common.parse(test2, Almanac))
    print(f"Part 2: {answer2}")
    assert answer2 == 46
