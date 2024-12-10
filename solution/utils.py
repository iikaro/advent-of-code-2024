from typing import Any, Iterable

NUMBERS: list[str] = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


def print_solution(solution: Any) -> None:
    print(f"The solution is: {solution}.")


def convert_to_int(elements: Iterable[str]) -> list[int]:
    return [int(element) for element in elements if element in NUMBERS]
