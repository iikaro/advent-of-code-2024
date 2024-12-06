import copy
from enum import StrEnum
from itertools import cycle

import numpy as np

from input.manager import get_input
from solution.utils import print_solution

GUARD_CHAR_LIST: list[str] = ["^", ">", "v", "<"]
GUARD_CHAR_CYCLE = cycle(GUARD_CHAR_LIST)
OBSTRUCTIONS: list[str] = ["#", "O"]
VISITED_POSITION: str = "X"
FREE_SPOT: str = "."
TEST_INPUT: str = "....#.....\n.........#\n..........\n..#.......\n.......#..\n..........\n.#..^.....\n........#.\n#.........\n......#..."


class GuardStatus(StrEnum):
    ESCAPED = "escaped"
    STUCK = "stuck"


def load_map(data: str) -> np.ndarray:
    return np.array([list(row) for row in data.splitlines()])


def find_guard(matrix_map: np.ndarray) -> tuple[int, int]:
    for char in GUARD_CHAR_LIST:
        coordinates = np.where(matrix_map == char)
        if coordinates[0].size != 0:
            return int(coordinates[0][0]), int(coordinates[1][0])
    raise ValueError("No guard found")


_FRONT_COORDINATES_OFFSET_MAP: dict[str, tuple[int, int]] = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1),
}


def patrol(matrix_map: np.ndarray, start_row: int, start_column: int) -> tuple[set[tuple[int, int, str]], GuardStatus]:
    dimensions: tuple[int, int] = matrix_map.shape
    guard_char_cycle = cycle(GUARD_CHAR_LIST)
    guard_char = next(guard_char_cycle)
    row: int = start_row
    column: int = start_column
    visited_coordinates: set[tuple[int, int, str]] = set()
    obstruction_mask = np.isin(matrix_map, OBSTRUCTIONS)

    while True or len(visited_coordinates) > 10_000:
        # Add current guard coordinates and direction
        visited_coordinates.add((row, column, guard_char))

        # Read position in front of guard
        front_row = row + _FRONT_COORDINATES_OFFSET_MAP[guard_char][0]
        front_column = column + _FRONT_COORDINATES_OFFSET_MAP[guard_char][1]

        if (front_row, front_column, guard_char) in visited_coordinates:
            return visited_coordinates, GuardStatus.STUCK

        # Check if guard is out of bounds
        if front_row == dimensions[0] or front_row < 0 or front_column == dimensions[1] or front_column < 0:
            return visited_coordinates, GuardStatus.ESCAPED

        # Check if there is an obstruction
        if obstruction_mask[front_row, front_column]:
            # Rotate guard
            guard_char = next(guard_char_cycle)
            # Guard stays still
            front_row = row
            front_column = column

        row = front_row
        column = front_column

    return visited_coordinates, GuardStatus.STUCK


def is_obstruction(matrix_map: np.ndarray, row: int, column: int) -> bool:
    if matrix_map[row][column] in OBSTRUCTIONS:
        return True
    return False


def place_obstruction(matrix_map: np.ndarray, row: int, column: int) -> tuple[np.ndarray, True]:
    if matrix_map[row][column] == FREE_SPOT:
        matrix_map_with_obstruction = copy.deepcopy(matrix_map)
        matrix_map_with_obstruction[row, column] = "O"
        return matrix_map_with_obstruction, True
    return matrix_map, False


def test_part_1() -> None:
    data = TEST_INPUT
    matrix_map: np.ndarray = load_map(data)
    solution = count_visited_coordinates(matrix_map)
    print_solution(solution)
    assert solution == 41


def solve_part_1() -> None:
    data = get_input(day=6)
    matrix_map: np.ndarray = load_map(data)
    solution = count_visited_coordinates(matrix_map)
    print_solution(solution)
    assert solution == 5331


def count_visited_coordinates(matrix_map: np.ndarray) -> int:
    row, column = find_guard(matrix_map)
    visited_coordinates, guard_status = patrol(matrix_map, row, column)
    unique_coordinates = set((x, y) for x, y, direction in visited_coordinates)
    return len(unique_coordinates)


def test_part_2() -> None:
    data = TEST_INPUT
    matrix_map: np.ndarray = load_map(data)
    count = count_loops(matrix_map)
    print_solution(count)
    assert count == 6


def count_loops(matrix_map: np.ndarray) -> int:
    count: int = 0
    guard_row, guard_column = find_guard(matrix_map)
    for row in range(matrix_map.shape[0]):
        for column in range(matrix_map.shape[1]):
            matrix_map_with_obstruction, is_map_updated = place_obstruction(matrix_map, row, column)
            if is_map_updated:
                visited_coordinates, guard_status = patrol(matrix_map_with_obstruction, guard_row, guard_column)
                print(f"Obstacle in ({row},{column}), guard_status={guard_status}")
                if guard_status == GuardStatus.STUCK:
                    count += 1
    return count


def solve_part_2() -> None:
    data = get_input(day=6)
    matrix_map: np.ndarray = load_map(data)
    count = count_loops(matrix_map)
    print_solution(count)


if __name__ == "__main__":
    test_part_1()
    solve_part_1()
    test_part_2()
    solve_part_2()
