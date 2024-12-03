import re
from functools import reduce

from input.manager import get_input
from solution.utils import print_solution

_TEST_INPUT = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"


def find_matches(text: str) -> list[tuple]:
    pattern = r"mul\((\d+\,\d+)\)"
    return re.findall(pattern, text)


def parse_to_int(data: list[str]) -> list[int]:
    return [int(number) for number_pair in data for number in number_pair.split(",")]


def multiply_and_sum(numbers: list[int]) -> int:
    result = 0
    for i in range(1, len(numbers), 2):
        result += numbers[i] * numbers[i - 1]
    return result


def post_process_input(text: str) -> str:
    pattern = r"do\(\)(.*?)don't\(\)"
    # Inject do() at the start (since it is implicit)
    data = "do()" + text + "don't()"
    matches = re.findall(pattern, data)
    return "".join(matches)


if __name__ == "__main__":
    # Test
    solution = reduce(lambda x, f: f(x), [find_matches, parse_to_int, multiply_and_sum], _TEST_INPUT)
    assert solution == 161

    # Part 1
    data = "".join(get_input(day=3))
    solution = reduce(lambda x, f: f(x), [find_matches, parse_to_int, multiply_and_sum], data)
    print_solution(solution)
    assert solution == 184576302

    # Test 2
    solution = reduce(lambda x, f: f(x), [post_process_input, find_matches, parse_to_int, multiply_and_sum], _TEST_INPUT)
    assert solution == 48

    # Part 2
    solution = reduce(lambda x, f: f(x), [post_process_input, find_matches, parse_to_int, multiply_and_sum], data)
    print_solution(solution)
    assert solution == 118173507
