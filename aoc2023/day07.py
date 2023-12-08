import enum
import collections
import typing as t
from dataclasses import dataclass

import common

lexmap = {
    "A": "m",
    "K": "l",
    "Q": "k",
    "J": "j",
    "T": "i",
    "9": "h",
    "8": "g",
    "7": "f",
    "6": "e",
    "5": "d",
    "4": "c",
    "3": "b",
    "2": "a",
}

wildmap = dict(lexmap)
wildmap["J"] = "0"


class HandType(enum.Enum):
    FiveOfAKind = 60
    FourOfAKind = 50
    FullHouse = 40
    ThreeOfAKind = 30
    TwoPair = 20
    OnePair = 10
    HighCard = 0


def to_hand_type(val: str) -> HandType:
    counts = collections.Counter(val)
    c = sorted((v for v in counts.values()), key=lambda v: -v)
    match c:
        case [5]:
            return HandType.FiveOfAKind
        case [4, 1]:
            return HandType.FourOfAKind
        case [3, 2]:
            return HandType.FullHouse
        case [3, 1, 1]:
            return HandType.ThreeOfAKind
        case [2, 2, 1]:
            return HandType.TwoPair
        case [2, 1, 1, 1]:
            return HandType.OnePair
        case [1, 1, 1, 1, 1]:
            return HandType.HighCard
    raise Exception("Unexpected card count!")


def to_wild_hand_type(val: str) -> HandType:
    counts = collections.Counter(val)
    c = sorted((v for r, v in counts.items() if r != "J"), key=lambda v: -v)
    wild = counts.get("J", 0)
    if c:
        c[0] += wild
    else:
        c = [wild]

    match c:
        case [5]:
            return HandType.FiveOfAKind
        case [4, 1]:
            return HandType.FourOfAKind
        case [4]:
            return HandType.FourOfAKind
        case [3, 2]:
            return HandType.FullHouse
        case [3, 1]:
            return HandType.ThreeOfAKind
        case [3, 1, 1]:
            return HandType.ThreeOfAKind
        case [2, 2, 1]:
            return HandType.TwoPair
        case [2, 2]:
            return HandType.TwoPair
        case [2, 1]:
            return HandType.OnePair
        case [2]:
            return HandType.OnePair
        case [2, 1, 1, 1]:
            return HandType.OnePair
        case [2, 1, 1]:
            return HandType.OnePair
        case [1, 1, 1, 1, 1]:
            return HandType.HighCard
    raise Exception("Unexpected card count!")


@dataclass
class Hand:
    hand: str
    lex: str
    hand_type: HandType
    bid: int

    @classmethod
    def from_lines(cls: type[t.Self], data_iter: t.Iterator[str]) -> t.Self:
        line = next(data_iter)
        hand, bid = line.split()
        return cls(hand, "".join(lexmap[c] for c in hand), to_hand_type(hand), int(bid))


@dataclass
class WildHand:
    hand: str
    lex: str
    hand_type: HandType
    bid: int

    @classmethod
    def from_lines(cls: type[t.Self], data_iter: t.Iterator[str]) -> t.Self:
        line = next(data_iter)
        hand, bid = line.split()
        return cls(hand, "".join(wildmap[c] for c in hand), to_wild_hand_type(hand), int(bid))


def part1(data: list[Hand]):
    return sum(hand.bid * rank for rank, hand in enumerate(sorted(data, key=lambda v: (v.hand_type.value, v.lex)), 1))


def part2(data: list[WildHand]):
    return sum(hand.bid * rank for rank, hand in enumerate(sorted(data, key=lambda v: (v.hand_type.value, v.lex)), 1))


def solution():
    raw_data = common.load("data/2023/day07.txt")

    formatted_data = common.parse(raw_data, Hand)
    answer1 = part1(formatted_data)
    print(f"Part 1: {answer1}")

    formatted_data = common.parse(raw_data, WildHand)
    answer2 = part2(formatted_data)
    print(f"Part 2: {answer2}")


def test():
    test1 = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""
    answer1 = part1(common.parse(test1, Hand))
    print(f"Part 1: {answer1}")
    assert answer1 == 6440

    test2 = test1
    answer2 = part2(common.parse(test2, WildHand))
    print(f"Part 2: {answer2}")
    assert answer2 == 5905
