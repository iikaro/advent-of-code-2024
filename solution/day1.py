from functools import reduce

from input.manager import get_input
from solution.utils import print_solution

TEST_INPUT = "3   4\n4   3\n2   5\n1   3\n3   9\n3   3\n"


def parse_input(data: list[str], delimiter: str = 3 * " ") -> list[list[int]]:
    return [[int(line.split(delimiter)[0]), int(line.split(delimiter)[1])] for line in data]


def sort_columns(data: list[list[int]]) -> list[list[int]]:
    return [sorted([pair[0] for pair in data]), sorted([pair[1] for pair in data])]


def compute_distance(data: list[list[int]]) -> int:
    return sum([abs(data[0][i] - data[1][i]) for i in range(0, len(data[0]))])


def compute_similarity(data: list[list[int]]) -> int:
    return sum([data[0][i] * data[1].count(data[0][i]) for i in range(0, len(data[0]))])


if __name__ == "__main__":
    # Test
    test_input_parsed = parse_input(TEST_INPUT.splitlines())
    test_input_sorted = sort_columns(test_input_parsed)
    distance = compute_distance(test_input_sorted)
    assert distance == 11

    # Part 1
    distance = reduce(lambda x, f: f(x), [parse_input, sort_columns, compute_distance], get_input(day=1))
    print_solution(distance)
    assert distance == 2164381

    # Part 2
    similarity_score = reduce(lambda x, f: f(x), [parse_input, sort_columns, compute_similarity], get_input(day=1))
    print_solution(similarity_score)
    assert similarity_score == 20719933
