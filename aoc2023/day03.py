import contextlib
import typing as t
from dataclasses import dataclass
from dataclasses import field

import common


@dataclass(frozen=True)
class Pos:
    x: int
    y: int


@dataclass
class Cell:
    character: str
    marked: bool = False
    gathered: bool = False
    number_id: int | None = None


@dataclass
class Schematic(common.LineConsumer):
    data: dict[Pos, Cell] = field(default_factory=dict)

    @classmethod
    def from_lines(cls: type[t.Self], data_iter: t.Iterator[str]) -> t.Self:
        s = cls()
        row = 0
        with contextlib.suppress(StopIteration):
            while line := next(data_iter):
                for col, char in enumerate(line):
                    if char != ".":
                        s.data[Pos(col, row)] = Cell(char)
                row += 1

        return s


def monotonic():
    i = 0
    while True:
        i += 1
        yield i


IDS = monotonic()


def is_symbol(cell: Cell):
    return not cell.character.isdigit()


def is_star_symbol(cell: Cell):
    return cell.character == "*"


def neigbours(pos: Pos):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i or j:
                yield Pos(pos.x + i, pos.y + j)


def gather_number(s: Schematic, p: Pos):
    offset = -1
    digits = []
    marked = False
    number_id = next(IDS)
    while (gather := Pos(p.x + offset, p.y)) in s.data and not is_symbol(s.data[gather]):
        cell = s.data[gather]
        cell.gathered = True
        cell.number_id = number_id
        digits.insert(0, cell.character)
        marked = marked or cell.marked
        offset -= 1

    offset = 0
    while (gather := Pos(p.x + offset, p.y)) in s.data and not is_symbol(s.data[gather]):
        cell = s.data[gather]
        cell.gathered = True
        cell.number_id = number_id
        digits.append(cell.character)
        marked = marked or cell.marked
        offset += 1

    return int("".join(digits)), marked


def gather_marked_numbers(s: Schematic):
    gathered: list[int] = []
    for pos in s.data:
        if s.data[pos].gathered or is_symbol(s.data[pos]):
            continue

        # it's a digit we haven't seen yet
        num, marked = gather_number(s, pos)
        if marked:
            gathered.append(num)

    return gathered


def part1(s: Schematic):
    for pos, cell in s.data.items():
        if is_symbol(cell):
            for neighbour in neigbours(pos):
                if neighbour in s.data:
                    s.data[neighbour].marked = True

    return sum(gather_marked_numbers(s))


def part2(s: Schematic):
    ratios = []

    # do a pass to generate ids
    for pos, cell in s.data.items():
        if is_symbol(cell) or cell.gathered:
            continue
        gather_number(s, pos)

    # for pos, cell in s.data.items():
    #     print(pos, cell)

    for pos, cell in s.data.items():
        if is_star_symbol(cell):
            count = len({s.data[neighbour].number_id for neighbour in neigbours(pos) if neighbour in s.data})
            is_gear = count == 2
            # print(f"found * at {pos}: {is_gear}")
            if is_gear:
                ratio_parts = set()
                for neighbour in neigbours(pos):
                    if neighbour in s.data:
                        # if s.data[neighbour].marked:
                        #     raise Exception("Gear twice!")
                        # s.data[neighbour].marked = True
                        ratio_parts.add(gather_number(s, neighbour)[0])
                part1 = ratio_parts.pop()
                part2 = ratio_parts.pop() if ratio_parts else part1
                ratios.append(part1 * part2)
    return sum(ratios)


def solution():
    raw_data = common.load("data/2023/day03.txt")
    formatted_data = common.parse_all(raw_data, Schematic)

    answer1 = part1(formatted_data)
    print(f"Part 1: {answer1}")

    answer2 = part2(formatted_data)
    print(f"Part 2: {answer2}")


def test():
    test1 = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
    answer1 = part1(common.parse_all(test1, Schematic))
    print(f"Part 1: {answer1}")
    assert answer1 == 4361

    answer2 = part2(common.parse_all(test1, Schematic))
    print(f"Part 2: {answer2}")
    assert answer2 == 467835
