import copy

import numpy as np

from input.manager import get_input_lines
from solution.utils import print_solution

_TEST_INPUT_1: str = "MMMSXXMASM\nMSAMXMSMSA\nAMXSXMAAMM\nMSAMASMSMX\nXMASAMXAMM\nXXAMMXXAMA\nSMSMSASXSS\nSAXAMASAAA\nMAMMMXMMMM\nMXMXAXMASX"

_TEST_INPUT_2: str = ".M.S......\n..A..MSMS.\n.M.S.MAA..\n..A.ASMSM.\n.M.S.M....\n..........\nS.S.S.S.S.\n.A.A.A.A..\nM.M.M.M.M.\n.........."

XMAS_HORIZONTAL = ["XMAS", "SAMX"]

MASK: list[list[bool]] = [
    [True, False, True],
    [False, True, False],
    [True, False, True],
]

XMAS_PATTERNS: list[str] = ["SSAMM", "MSAMS", "MMASS", "SMASM"]

OFFSET_X: int = 3

OFFSET_Y: int = 3


def count_instances(data: str) -> int:
    count: int = 0
    count += count_horizontal_instances(data)
    count += count_horizontal_instances(transpose(data))
    count += count_diagonal_instances(data)
    return count


def transpose(data: str) -> str:
    lines: list[str] = data.splitlines()
    return '\n'.join([''.join(char) for char in zip(*lines)])


def delete_first_column_and_last_row(data: str) -> str:
    return "\n".join([row[1:] for row in data.splitlines()][:-1])


def delete_last_column_and_first_row(data: str) -> str:
    return "\n".join([row[:-1] for row in data.splitlines()][1:])


def delete_edge_rows_and_columns(data: str) -> str:
    return "\n".join([row[1:-1] for row in data.splitlines()][1:-1])


def count_diagonal_instances(data: str) -> int:
    count: int = count_main_diagonal_instances(data)
    count += count_main_diagonal_instances(reverse_data(data))
    return count


def count_main_diagonal_instances(data: str) -> int:
    current_data: str = copy.deepcopy(data)
    count: int = 0

    count += count_horizontal_instances(extract_diagonal(current_data))
    current_data_down = current_data
    current_data_up = current_data

    i: int = 0
    while i < len(data.splitlines()) - 1:
        # Move diagonal up
        current_data_up = delete_first_column_and_last_row(current_data_up)
        diagonal = extract_diagonal(current_data_up)
        count += count_horizontal_instances(diagonal)

        # Move diagonal down
        current_data_down = delete_last_column_and_first_row(current_data_down)
        diagonal = extract_diagonal(current_data_down)
        count += count_horizontal_instances(diagonal)

        i += 1
    return count


def reverse_data(data: str) -> str:
    return "\n".join([row[::-1] for row in data.splitlines()])


def extract_diagonal(data: str) -> str:
    return "".join([line[i] for i, line in enumerate(data.splitlines())])


def count_horizontal_instances(data: str) -> int:
    return sum([line.count(word) for word in XMAS_HORIZONTAL for line in data.split("\n")])


def test_part_1():
    data: str = _TEST_INPUT_1
    count: int = count_instances(data)
    assert count == 18


def solve_part_1():
    data: str = "\n".join(get_input_lines(day=4))
    count: int = count_instances(data)
    print_solution(count)
    assert count == 2406


def solve_part_2():
    count: int = count_xmas_patterns("\n".join(get_input_lines(day=4)))
    print_solution(count)
    assert count == 1807


def test_part_2():
    count: int = count_xmas_patterns(_TEST_INPUT_2)
    assert count == 9


def count_xmas_patterns(data: str):
    matrix: np.ndarray = np.array([list(row) for row in data.splitlines()])
    mask: np.ndarray = np.array(MASK, dtype=np.bool)
    count: int = 0
    columns: int = matrix.shape[1]
    rows: int = matrix.shape[0]
    i: int = 0
    while i < rows - 2:
        j: int = 0
        while j < columns - 2:
            matrix_slice: list[str] = matrix[i:i + OFFSET_X, j: j + OFFSET_Y][mask].tolist()
            if check_if_mask_matches_pattern(matrix_slice):
                count += 1
            j += 1
        i += 1
    return count


def check_if_mask_matches_pattern(masked_values: list[str], patterns: list[str] = None) -> bool:
    patterns: list[str] = patterns or XMAS_PATTERNS
    if "".join(masked_values) in patterns:
        return True
    return False


if __name__ == "__main__":
    test_part_1()
    solve_part_1()
    test_part_2()
    solve_part_2()
