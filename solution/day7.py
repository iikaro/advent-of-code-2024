import copy
from collections import namedtuple
from operator import add, mul
from typing import Callable

from input.manager import get_input
from solution.utils import print_solution

TEST_INPUT: str = "190: 10 19\n3267: 81 40 27\n83: 17 5\n156: 15 6\n7290: 6 8 6 15\n161011: 16 10 13\n192: 17 8 14\n21037: 9 7 18 13\n292: 11 6 16 20"

Equation = namedtuple("Equation", ["result", "arguments"])


def concatenate(a, b):
    return int(str(a) + str(b))


OPERATORS = [add, mul, concatenate]


def parse_to_int(data: list[str]) -> list[int]:
    return [int(number) for number in data]


def parse_input_to_named_tuple(data: str) -> list[Equation]:
    equations: list[str] = data.splitlines()
    equations_data: list[list[str]] = [equation.split(":") for equation in equations]
    arguments: list[list[int]] = [parse_to_int(equation_data[1].split()) for equation_data in equations_data]
    results: list[int] = [int(equation_data[0]) for equation_data in equations_data]
    return [Equation(result, arguments) for result, arguments in zip(results, arguments)]


def check_if_operation_is_possible(equation: Equation, operators: list[Callable]) -> int:
    arguments = copy.deepcopy(equation.arguments)
    values = [arguments[0]]
    for i in range(0, len(arguments) - 1):
        argument = arguments[i + 1]
        next_values = []
        for value in values:
            next_values += [function(value, argument) for function in operators]
        values = next_values
    if equation.result in values:
        return equation.result
    return 0


def sum_possible_operations_results(data: str, operators: list[Callable] = None) -> int:
    if not operators:
        operators = [add, mul]
    equations: list[Equation] = parse_input_to_named_tuple(data)
    result: int = 0
    for i, equation in enumerate(equations):
        result += check_if_operation_is_possible(equation, operators)
    return result


def test_part_1() -> None:
    data: str = TEST_INPUT
    solution: int = sum_possible_operations_results(data)
    print_solution(solution)
    assert solution == 3749


def solve_part_1() -> None:
    data: str = get_input(day=7)
    solution: int = sum_possible_operations_results(data)
    print_solution(solution)
    assert solution == 465126289353


def test_part_2() -> None:
    data: str = TEST_INPUT
    solution: int = sum_possible_operations_results(data, OPERATORS)
    print_solution(solution)
    assert solution == 11387


def solve_part_2() -> None:
    data: str = get_input(day=7)
    solution: int = sum_possible_operations_results(data, OPERATORS)
    print_solution(solution)
    assert solution == 70597497486371


if __name__ == "__main__":
    test_part_1()
    test_part_2()
    solve_part_1()
    solve_part_2()
