from utils import load

digits_as_words = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def parse(raw_data):
    return raw_data.splitlines()


def make_digits(row: str, index: int) -> int:
    if row[index].isdigit():
        return int(row[index])

    for digit in digits_as_words:
        if row[index : index + len(digit)] == digit:
            return digits_as_words[digit]

    return 0


def part1(data):
    sum = 0
    for row in data:
        numbers = [c for c in row if c.isdigit()]
        sum += int(f"{numbers[0]}{numbers[-1]}")

    return sum


def part2(data):
    sum = 0
    for row in data:
        numbers = [processed for i in range(len(row)) if (processed := make_digits(row, i))]
        sum += int(f"{numbers[0]}{numbers[-1]}")

    return sum


def solution():
    raw_data = load("data/2023/day01.txt")
    formatted_data = parse(raw_data)

    answer1 = part1(formatted_data)
    print(f"Part 1: {answer1}")

    answer2 = part2(formatted_data)
    print(f"Part 2: {answer2}")


def test():
    test1 = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""
    answer1 = part1(parse(test1))
    print(f"Part 1: {answer1}")
    assert answer1 == 142

    test2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""
    answer2 = part2(parse(test2))
    print(f"Part 2: {answer2}")
    assert answer2 == 281
