from typing import Tuple

import numpy as np

from input.manager import get_input
from solution.utils import convert_to_int, print_solution

TEST_INPUT: str = "89010123\n78121874\n87430965\n96549874\n45678903\n32019012\n01329801\n10456732"
TRAILHEAD: str = "0"
MAX_HEIGHT: int = 9


def find_path(data: str, check_visited_coords: bool = True) -> int:
    topographic_map: list[list[int]] = [convert_to_int(list(row)) for row in data.splitlines()]
    start_trailheads: set[tuple[int, int]] = set(
        [
            (i, j)
            for i in range(len(topographic_map))
            for j in range(len(topographic_map[0]))
            if topographic_map[i][j] == int(TRAILHEAD)
        ],
    )

    limits: tuple[int, int] = len(topographic_map), len(topographic_map[0])
    total_sum: int = 0
    for trailhead in sorted(start_trailheads):
        score: list[int] = []
        visited_coords: set[tuple[int, int]] = set()
        check_surroundings(score, trailhead, visited_coords, topographic_map, limits, check_visited_coords)
        print(f"Trailhead at {trailhead} has a score of {sum(score)}")
        total_sum += sum(score)
    return total_sum


def check_surroundings(
    score: list[int],
    trailhead: tuple[int, int],
    visited_coords: set[tuple[int, int]],
    topographic_map: list[list[int]],
    limits: tuple[int, int],
    check_visited_coords: bool = True,
) -> None:
    # Compute height
    height: int = topographic_map[trailhead[0]][trailhead[1]]

    if check_visited_coords:
        if trailhead in visited_coords:
            return
        visited_coords.add(trailhead)

    # Check if max height has been achieved
    if height == MAX_HEIGHT:
        score.append(1)
        return

    # Define directions
    directions = [
        (trailhead[0] - 1, trailhead[1]),  # Up
        (trailhead[0], trailhead[1] + 1),  # Right
        (trailhead[0] + 1, trailhead[1]),  # Down
        (trailhead[0], trailhead[1] - 1),  # Left
    ]

    # Explore all valid directions
    for next_position in directions:
        if is_within_limits(next_position, limits):
            next_height = topographic_map[next_position[0]][next_position[1]]
            if is_slope_gradual(next_height, height):
                # Recursive call with shared visited set
                check_surroundings(score, next_position, visited_coords, topographic_map, limits, check_visited_coords)


def is_within_limits(coordinates: tuple[int, int], limits: tuple[int, int]) -> bool:
    return 0 <= coordinates[0] < limits[0] and 0 <= coordinates[1] < limits[1]


def is_slope_gradual(next_height: int, current_height: int) -> bool:
    return next_height == current_height + 1


def test_part_1() -> None:
    solution = find_path(TEST_INPUT)
    print_solution(solution)
    assert solution == 36


def solve_part_1() -> None:
    solution = find_path(get_input(day=10))
    print_solution(solution)
    assert solution == 617


def test_part_2() -> None:
    solution = find_path(TEST_INPUT, False)
    print_solution(solution)
    assert solution == 81


def solve_part_2() -> None:
    solution = find_path(get_input(day=10), False)
    print_solution(solution)
    assert solution == 617


if __name__ == "__main__":
    test_part_1()
    solve_part_1()
    test_part_2()
    solve_part_2()
