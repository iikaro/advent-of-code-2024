from typing import Any, Iterable


def print_solution(solution: Any) -> None:
    print(f"The solution is: {solution}.")


def convert_to_int(elements: Iterable[str]) -> list[int]:
    return [int(element) for element in elements]
