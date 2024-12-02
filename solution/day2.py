import copy

from input.manager import get_input
from solution.utils import print_solution

_TEST_INPUT = "7 6 4 2 1\n1 2 7 8 9\n9 7 6 2 1\n1 3 2 4 5\n8 6 4 4 1\n1 3 6 7 9"


def parse_input(data: list[str]) -> list[list[int]]:
    lines: list[list[str]] = [line.split() for line in data]
    data: list[list[int]] = []
    for line in lines:
        data.append([int(number) for number in line])
    return data


def check_numbers_are_monotonic(report: list[int]) -> list[int]:
    is_increasing = report[1] - report[0] > 0
    checked_levels = []
    for i in range(2, len(report)):
        if (report[i] > report[i - 1]) == is_increasing:
            checked_levels.append(report[i])
    return checked_levels


def check_distance(report: list[int]) -> list[int]:
    checked_levels = []
    for i in range(1, len(report)):
        if 0 < abs(report[i] - report[i - 1]) <= 3:
            checked_levels.append(report[i])
    return checked_levels


def check_level_is_safe(report: list[int]) -> bool:
    is_distance_safe = len(check_distance(report)) == len(report) - 1
    is_monotonicity_safe = len(check_numbers_are_monotonic(report)) == len(report) - 2
    return is_distance_safe and is_monotonicity_safe


def check_level_is_safe_with_tolerance(report: list[int]) -> bool:
    # Check if report is unsafe
    if not check_level_is_safe(report):
        # Try to check if the report, without one level, becomes safe
        for i in range(0, len(report)):
            new_report = copy.deepcopy(report)
            new_report.pop(i)
            if check_level_is_safe(new_report):
                return True
    return check_level_is_safe(report)


if __name__ == "__main__":
    # Test
    test_levels = parse_input(_TEST_INPUT.splitlines())
    is_safe = [check_level_is_safe(level) for level in test_levels]
    test_total_safe_levels = sum(is_safe)
    assert test_total_safe_levels == 2

    # Part 1
    total_safe_levels = sum([check_level_is_safe(report) for report in parse_input(get_input(day=2))])
    print_solution(total_safe_levels)
    assert total_safe_levels == 663

    # Test
    test_levels = parse_input(_TEST_INPUT.splitlines())
    is_safe = [check_level_is_safe_with_tolerance(level) for level in test_levels]
    test_total_safe_levels = sum(is_safe)
    assert test_total_safe_levels == 4

    # Part 2
    total_safe_levels = sum([check_level_is_safe_with_tolerance(report) for report in parse_input(get_input(day=2))])
    print_solution(total_safe_levels)
    assert total_safe_levels == 692
