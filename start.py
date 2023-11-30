import datetime
from pathlib import Path
import os

import requests

from utils import load


def load_cookie(cookie: str) -> str:
    cookie_path = Path("data/cookie")
    return load(cookie_path / cookie).strip()


def main():
    now = datetime.datetime.now()
    now = datetime.datetime(2022, 12, 5)

    data_path = Path(f"data/{now.year}/day{now.strftime("%d")}.txt")
    problem_path = Path(f"aoc{now.year}/day{now.strftime("%d")}.py")
    input_path = f"https://adventofcode.com/{now.year}/day/{now.day}/input"
    response = requests.get(input_path, cookies={"session": load_cookie("session")})
    assert response.status_code == 200, f"Got unexpected response status: {response.status_code}"

    os.makedirs(data_path.parent, exist_ok=True)
    with open(data_path, "w") as fp:
        fp.write(response.content.decode("utf-8"))

    os.makedirs(problem_path.parent, exist_ok=True)
    with open(problem_path, "w") as fp:
        fp.write(load("template.py").format(year=now.year, day=now.day))


if __name__ == "__main__":
    main()