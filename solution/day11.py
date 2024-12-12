from functools import cache

from solution.utils import print_solution

TEST_INPUT: str = "0 1 10 99 999"
MAX_BLINKS: int = 25


@cache
def is_number_digits_count_is_even(number: str) -> bool:
    return len(number) % 2 == 0


@cache
def split_number_into_two(number: str) -> tuple[str, str]:
    length: int = len(number)
    left_number: str = str(int(number[: length // 2]))
    right_number: str = str(int(number[length // 2 :]))
    return left_number, right_number


@cache
def apply_rules(stone: str) -> list[str]:
    if stone == "0":
        return ["1"]
    if is_number_digits_count_is_even(stone):
        left_number, right_number = split_number_into_two(stone)
        return [left_number, right_number]
    else:
        return [str(int(stone) * 2024)]


@cache
def blink_in_front_of_stones(stone: str, blinks: int) -> 1:
    if blinks == 0:
        return 1
    stones = apply_rules(stone)
    return sum([blink_in_front_of_stones(stone, blinks - 1) for stone in stones])


def test_part_1() -> None:
    data: str = "125 17"
    stones: list[str] = [number for number in data.split()]
    count: int = 0
    for stone in stones:
        count += blink_in_front_of_stones(stone, 6)
    solution: int = count
    print_solution(solution)
    assert solution == 22


def solve_part_1() -> None:
    data: str = "1117 0 8 21078 2389032 142881 93 385"
    stones: list[str] = [number for number in data.split()]
    count: int = 0
    for stone in stones:
        count += blink_in_front_of_stones(stone, 25)
    solution: int = count
    print_solution(solution)
    assert solution == 224529


def solve_part_2() -> None:
    data: str = "1117 0 8 21078 2389032 142881 93 385"
    stones: list[str] = [number for number in data.split()]
    count: int = 0
    for stone in stones:
        count += blink_in_front_of_stones(stone, 75)
    solution: int = count
    print_solution(solution)
    assert solution == 266820198587914


if __name__ == "__main__":
    test_part_1()
    solve_part_1()
    solve_part_2()
