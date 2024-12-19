from __future__ import annotations
import contextlib
import typing as t
from dataclasses import dataclass
from dataclasses import field
import heapq

import common


@dataclass
class ParsedCoord(common.LineConsumer):
    """A single line, with a single data member containing the whole string."""

    pos: Coordinate

    @classmethod
    def from_lines(cls: t.Type[t.Self], data_iter: t.Iterator[str]) -> t.Self:
        line = next(data_iter)
        x, y = line.split(",")
        return cls(Coordinate(int(x), int(y)))


@dataclass
class Grid:
    grid: dict[Coordinate, str] = field(default_factory=dict)

    def clone(self):
        return Grid(self.grid.copy())

    def add(self, pos: Coordinate, cell: str):
        self.grid[pos] = cell

    def remove(self, pos: Coordinate):
        return self.grid.pop(pos, None)

    def at(self, pos: Coordinate) -> str | None:
        return self.grid.get(pos)

    def print(
        self: Grid,
        visited: dict[tuple[Coordinate, Coordinate], int],
        edges: list[tuple[int, Coordinate, Coordinate]],
    ):
        visited_set = {c for c, _ in visited}
        edge_set = {c for _, __, c in edges}
        size = Coordinate(0, 0)
        for coord in self.grid:
            size = max(size, coord)
        for y in range(size.y + 2):
            for x in range(size.x + 2):
                pos = Coordinate(x, y)
                if pos in edge_set:
                    print("0", end="")
                    continue
                if pos in visited_set:
                    print("X", end="")
                    continue
                val = self.at(pos)
                if val:
                    print(val, end="")
                else:
                    print("#", end="")
            print()


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def __add__(self, other: Coordinate):
        return Coordinate(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Coordinate):
        return Coordinate(self.x - other.x, self.y - other.y)

    def __mul__(self, other: int):
        return Coordinate(self.x * other, self.y * other)

    def __lt__(self, other: Coordinate) -> bool:
        return (self.x, self.y) < (other.x, other.y)

    def __mod__(self, other: Coordinate):
        return Coordinate(self.x % other.x, self.y % other.y)


def navigate(start: Coordinate, end: Coordinate, grid: Grid, any_path: bool = False):
    heading = E
    min_cost = 9_999_999_999
    visited: dict[tuple[Coordinate, Coordinate], int] = {}
    edges: list[tuple[int, Coordinate, Coordinate]] = []
    heapq.heappush(edges, (0, heading, start))
    # bail = 100
    while edges:
        # print(edges)
        cost, in_heading, pos = heapq.heappop(edges)
        # print("visiting", pos, cost, heading)
        prev_cost = visited.get((pos, in_heading), 9_999_999_999)
        visited[pos, in_heading] = min(cost, prev_cost)
        # print("set visisted at", pos, "to", visited[pos, in_heading])
        if prev_cost <= cost:
            continue
        if pos == end:
            # print(f"Found the end!")
            # grid.print(visited, edges)
            min_cost = min(min_cost, cost)
            if any_path:
                return min_cost
        else:
            for neighbor, new_heading, next_cost in neighbor_coords(pos, in_heading):
                if grid.at(neighbor) is None:
                    # print("discarding(1)", neighbor)
                    if neighbor == Coordinate(x=139, y=1):
                        # print("discarded(1) the end as a neighbor")
                        pass
                    continue
                if visited.get((neighbor, new_heading), 9_999_999_999) > cost + next_cost:
                    # print("adding", cost + next_cost, new_heading, neighbor)
                    if neighbor == Coordinate(x=139, y=1):
                        # print("added the end as a neighbor")
                        pass
                    heapq.heappush(edges, (cost + next_cost, new_heading, neighbor))
                else:
                    if neighbor == Coordinate(x=139, y=1):
                        # print(
                        #     "discarded(2) the end as a neighbor",
                        #     visited.get((neighbor, new_heading), 9_999_999_999),
                        #     "<=",
                        #     cost + next_cost,
                        # )
                        pass
                    # print("discarding(2)", neighbor)
                    pass
        # grid.print(visited, edges)
        # if not bail:
        #     print("yes, we bail")
        #     break
        # bail -= 1
    # grid.print(visited, edges)
    return min_cost


def cardinals():
    yield from [
        Coordinate(0, -1),
        Coordinate(1, 0),
        Coordinate(0, 1),
        Coordinate(-1, 0),
    ]


cardinal_list = [c for c in cardinals()]
N, E, S, W = cardinal_list
turns = {
    # dir: (ccw, cw)
    N: (W, E),
    E: (N, S),
    S: (E, W),
    W: (S, N),
}


def neighbor_coords(pos: Coordinate, heading: Coordinate):
    yield pos + heading, heading, 1
    ccw, cw = turns[heading]
    yield pos + ccw, ccw, 1
    yield pos + cw, cw, 1


def part1(data: t.Sequence[ParsedCoord], size=70, count=1024):
    memory = Grid()
    start = Coordinate(0, 0)
    end = Coordinate(size, size)
    for j in range(size + 1):
        for i in range(size + 1):
            memory.add(Coordinate(i, j), ".")

    for i in range(count):
        memory.remove(data[i].pos)

    return navigate(start, end, memory)


def part2(data: t.Sequence[ParsedCoord], size=70, count=1024):
    memory = Grid()
    start = Coordinate(0, 0)
    end = Coordinate(size, size)
    max_steps = (count + 1) ** 2
    for j in range(size + 1):
        for i in range(size + 1):
            memory.add(Coordinate(i, j), ".")

    for i in range(count):
        memory.remove(data[i].pos)

    print(len(data))
    for i in range(count, len(data)):
        memory.remove(data[i].pos)
        print(i, data[i].pos)
        next_try = navigate(start, end, memory)
        if next_try > max_steps:
            return data[i].pos

    return 0


def solution():
    raw_data = common.load("data/2024/day18.txt")
    # See also `common.pares_all` for more complicated inputs
    formatted_data = common.parse(raw_data, ParsedCoord)

    answer1 = part1(formatted_data)
    print(f"Part 1: {answer1}")

    answer2 = part2(formatted_data)
    print(f"Part 2: {answer2}")


def test():
    test1 = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""
    answer1 = part1(common.parse(test1, ParsedCoord), 6, 12)
    print(f"Part 1: {answer1}")
    # assert answer1 == ???

    test2 = test1
    answer2 = part2(common.parse(test2, ParsedCoord), 6, 12)
    print(f"Part 2: {answer2}")
    # assert answer2 == ???
