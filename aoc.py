import datetime
import importlib
import sys
import typing as t

RunKind = t.Literal["run", "test"]
run_kinds = t.get_args(RunKind)


def is_run_kind(val: str) -> t.TypeGuard[RunKind]:
    return val in run_kinds


def main():
    try:
        program_name, kind, *args = sys.argv
        if not is_run_kind(kind):
            raise ValueError(f"Invalid RunKind {kind}")
    except ValueError:
        print("usage: python -m aoc [run|test] <day> <year>")
        sys.exit(1)

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
        if kind == "test":
            m.test()
        else:
            m.solution()
    except ImportError:
        print(f"Unable to find AOC {year}, Day {day:02}")


if __name__ == "__main__":
    main()
