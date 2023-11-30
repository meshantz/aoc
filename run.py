import datetime
import importlib
import sys


def main():
    program_name, *args = sys.argv
    now = datetime.datetime.now()
    match args:
        case [day, year]:
            day = int(day)
            year = int(year)
        case [day]:
            day = int(day)
            year = now.year
        case _:
            day = now.day
            year = now.year

    try:
        m = importlib.import_module(f"aoc{year}.day{day:02}")
        print(f"Running AOC {year}, Day {day:02}")
        m.solution()
    except ImportError:
        print(f"Unable to find AOC {year}, Day {day:02}")


if __name__ == "__main__":
    main()
