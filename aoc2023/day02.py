import typing as t
from dataclasses import dataclass

import common


@dataclass
class CubeGame(common.LineConsumer):
    game_id: int
    reveals: list[dict]

    @classmethod
    def from_lines(cls: type[t.Self], data_iter: t.Iterator[str]) -> t.Self:
        game = next(data_iter)
        game_id_part, reveals_part = game.split(":")
        game_id = int(game_id_part.split()[1])

        reveal_list = reveals_part.split(";")
        reveals = []
        for reveal in reveal_list:
            groups = reveal.split(",")
            reveal_dict = {}
            for group in groups:
                count, color = group.split()
                reveal_dict[color.strip()] = int(count)
            reveals.append(reveal_dict)

        return cls(game_id, reveals)

    def possible(self, *, red: int, green: int, blue: int):
        for reveal in self.reveals:
            if red < reveal.get("red", 0):
                return False
            if green < reveal.get("green", 0):
                return False
            if blue < reveal.get("blue", 0):
                return False
        return True

    def fewest(self):
        f = {"red": 0, "green": 0, "blue": 0}
        for reveal in self.reveals:
            for color in {"red", "green", "blue"}:
                f[color] = max(f[color], reveal.get(color, 0))
        return f

    def power(self):
        f = self.fewest()
        return f["red"] * f["green"] * f["blue"]


def part1(data: list[CubeGame]):
    return sum(d.game_id for d in data if d.possible(red=12, green=13, blue=14))


def part2(data: list[CubeGame]):
    return sum(d.power() for d in data)


def solution():
    raw_data = common.load("data/2023/day02.txt")
    formatted_data = common.parse(raw_data, CubeGame)

    answer1 = part1(formatted_data)
    print(f"Part 1: {answer1}")

    answer2 = part2(formatted_data)
    print(f"Part 2: {answer2}")


def test():
    test_data = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
    answer1 = part1(common.parse(test_data, CubeGame))
    print(f"Part 1: {answer1}")
    assert answer1 == 8

    answer2 = part2(common.parse(test_data, CubeGame))
    print(f"Part 2: {answer2}")
    assert answer2 == 2286
