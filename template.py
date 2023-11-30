from utils import load


def parse(raw_data):
    return raw_data


def part1(data):
    return 0


def part2(data):
    return 0


def solution():
    raw_data = load("data/{year}/day{day:02}.txt")
    formatted_data = parse(raw_data)

    answer1 = part1(formatted_data)
    print(f"Part 1: {{answer1}}")

    answer2 = part2(formatted_data)
    print(f"Part 2: {{answer2}}")