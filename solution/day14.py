import dataclasses
from functools import cache

from input.manager import get_input
from solution.utils import print_solution

TEST_INPUT = "p=0,4 v=3,-3\np=6,3 v=-1,-3\np=10,3 v=-1,2\np=2,0 v=2,-1\np=0,0 v=1,3\np=3,0 v=-2,-2\np=7,6 v=-1,-3\np=3,0 v=-1,-2\np=9,3 v=2,3\np=7,3 v=-1,2\np=2,4 v=2,-3\np=9,5 v=-3,-3"
SPACE_X: int = 101
SPACE_Y: int = 103


@dataclasses.dataclass
class Position:
    x: int
    y: int

    def __hash__(self) -> int:
        return hash((self.x, self.y))


@dataclasses.dataclass
class Velocity:
    vx: int
    vy: int

    def __hash__(self) -> int:
        return hash((self.vx, self.vy))


@dataclasses.dataclass
class Robot:
    position: Position
    velocity: Velocity


def parse_input(data: str) -> list[Robot]:
    robots: list[Robot] = [
        Robot(
            position=Position(
                x=int(robot_data.split()[0].replace("p=", "").split(",")[0]),
                y=int(robot_data.split()[0].replace("p=", "").split(",")[1]),
            ),
            velocity=Velocity(
                vx=int(robot_data.split()[1].replace("v=", "").split(",")[0]),
                vy=int(robot_data.split()[1].replace("v=", "").split(",")[1]),
            ),
        )
        for robot_data in data.splitlines()
    ]
    return robots


def move_robots(robots: list[Robot], seconds: int, map_limits: tuple[int, int]) -> list[Robot]:
    while seconds > 0:
        for robot in robots:
            position: Position = compute_new_position(robot.position, robot.velocity, map_limits)
            robot.position = position
        seconds -= 1
    return robots


@cache
def compute_new_position(position: Position, velocity: Velocity, map_limits: tuple[int, int]) -> Position:
    x = (position.x + velocity.vx) % map_limits[0]
    y = (position.y + velocity.vy) % map_limits[1]
    return Position(x=x, y=y)


def get_map_with_robots(robots: list[Robot], map_limits: tuple[int, int], show: bool = False) -> list[list[int]]:
    tiles: list[list[int]] = [map_limits[0] * [0] for i in range(map_limits[1])]

    for robot in robots:
        tiles[robot.position.y][robot.position.x] += 1
    if show:
        for tile in tiles:
            print(tile)
    return tiles


def count_robots_per_quadrant(tiles: list[list[int]], map_limits: tuple[int, int]) -> int:
    first: list[list[int]] = [row[: map_limits[0] // 2] for row in tiles[: map_limits[1] // 2]]
    second: list[list[int]] = [row[map_limits[0] // 2 + 1 :] for row in tiles[: map_limits[1] // 2]]
    third: list[list[int]] = [row[: map_limits[0] // 2] for row in tiles[map_limits[1] // 2 + 1 :]]
    fourth: list[list[int]] = [row[map_limits[0] // 2 + 1 :] for row in tiles[map_limits[1] // 2 + 1 :]]
    return (
        sum([sum(row) for row in first])
        * sum([sum(row) for row in second])
        * sum([sum(row) for row in third])
        * sum([sum(row) for row in fourth])
    )


def solve(data: str, seconds: int, map_limits: tuple[int, int]) -> int:
    robots: list[Robot] = parse_input(data)
    moved_robots: list[Robot] = move_robots(robots, seconds=seconds, map_limits=map_limits)
    tiles: list[list[int]] = get_map_with_robots(moved_robots, map_limits=map_limits)
    return count_robots_per_quadrant(tiles, map_limits=map_limits)


def test_part_1():
    solution: int = solve(TEST_INPUT, 100, map_limits=(11, 7))
    assert solution == 12


def solve_part_1():
    solution: int = solve(get_input(day=14), 100, map_limits=(SPACE_X, SPACE_Y))
    assert solution == 217328832


if __name__ == "__main__":
    test_part_1()
    solve_part_1()
