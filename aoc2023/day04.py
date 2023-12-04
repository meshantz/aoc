import typing as t
from dataclasses import dataclass

import common


@dataclass
class ScratchCard(common.LineConsumer):
    card_id: int
    winners: set[int]
    yours: list[int]
    count: int = 1

    @classmethod
    def from_lines(cls: type[t.Self], data_iter: t.Iterator[str]) -> t.Self:
        line = next(data_iter)
        header, data = line.split(":")
        card_id = int(header.split()[1].strip())
        winners, yours = data.split("|")
        return cls(card_id, {int(n) for n in winners.split()}, [int(n) for n in yours.split()])


def matches(card: ScratchCard):
    return sum(1 for v in card.yours if v in card.winners)


def value(card: ScratchCard):
    winners = matches(card)
    return 2 ** (winners - 1) if winners else 0


def part1(data: list[ScratchCard]):
    return sum(value(card) for card in data)


def part2(data: list[ScratchCard]):
    data_dict = {card.card_id: card for card in data}
    for card_id, card in data_dict.items():
        winners = matches(card)
        for i in range(winners):
            data_dict[card_id + i + 1].count += card.count

    return sum(card.count for card in data)


def solution():
    raw_data = common.load("data/2023/day04.txt")
    formatted_data = common.parse(raw_data, ScratchCard)

    answer1 = part1(formatted_data)
    print(f"Part 1: {answer1}")

    answer2 = part2(formatted_data)
    print(f"Part 2: {answer2}")


def test():
    test1 = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
    answer1 = part1(common.parse(test1, ScratchCard))
    print(f"Part 1: {answer1}")
    assert answer1 == 13

    test2 = test1
    answer2 = part2(common.parse(test2, ScratchCard))
    print(f"Part 2: {answer2}")
    assert answer2 == 30
