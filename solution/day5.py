import copy
import dataclasses

from input.manager import get_input
from solution.utils import convert_to_int

TEST_INPUT = "47|53\n97|13\n97|61\n97|47\n75|29\n61|13\n75|53\n29|13\n97|29\n53|29\n61|53\n97|53\n61|29\n47|13\n75|47\n97|75\n47|61\n75|61\n47|29\n75|13\n53|13\n\n75,47,61,53,29\n97,61,53,29,13\n75,29,13\n75,97,47,61,53\n61,13,29\n97,13,75,29,47"


@dataclasses.dataclass
class Update:
    pages: list[int]


class Rule:
    first: int
    second: int


def get_rules_and_updates(data: str) -> tuple[list[list[int]], list[list[int]]]:
    rules, updates = data.split("\n\n")
    return parse_process_rules_and_updates(rules, updates)


def parse_process_rules_and_updates(rules: str, updates: str) -> tuple[list[list[int]], list[list[int]]]:
    updates_parsed = [convert_to_int(pages) for update in updates.split("\n") for pages in [update.split(",")]]
    rules_parsed = [convert_to_int(numbers) for rule in rules.split("\n") for numbers in [rule.split("|")]]
    return rules_parsed, updates_parsed


def get_correctly_sorted_updates(rules, updates):
    correctly_sorted_updates = []
    for pages in updates:
        passing_rules = [check_rule(rule, pages) for rule in rules]
        if all(passing_rules):
            correctly_sorted_updates.append(pages)
    return remove_repeated_elements(correctly_sorted_updates)


def get_incorrectly_sorted_updates(rules: list[list[int]], updates: list[list[int]]) -> list[list[int]]:
    fixed_sorted_updates: list[list[int]] = []
    for pages in updates:
        append_to_list: bool = False
        current_pages: list[int] = copy.deepcopy(pages)
        reference_pages: list[int] = copy.deepcopy(current_pages)
        failing_rules: list[bool] = [not check_rule(rule, pages) for rule in rules]

        while any(failing_rules):
            failing_rule_index:int = next(i for i, failing_rule in enumerate(failing_rules) if failing_rule is True)
            append_to_list = True
            rule = rules[failing_rule_index]
            current_pages = copy.deepcopy(reference_pages)
            current_pages[reference_pages.index(rule[1])] = rule[0]
            current_pages[reference_pages.index(rule[0])] = rule[1]
            reference_pages = copy.deepcopy(current_pages)
            failing_rules = [not check_rule(rule, reference_pages) for rule in rules]

        if append_to_list:
            fixed_sorted_updates.append(current_pages)

    return fixed_sorted_updates


def remove_repeated_elements(updates: list[list[int]]) -> list[list[int]]:
    filtered_updates = []
    for pages in updates:
        if pages not in filtered_updates:
            filtered_updates += [pages]
    return filtered_updates


def check_rule(rule: list[int], pages: list[int]) -> bool:
    page_before: int = rule[0]
    page_after: int = rule[1]

    # Check if pages does NOT contain pages with rule
    if page_before not in pages or page_after not in pages:
        return True
    # Check if pages FOLLOW rule
    if pages.index(page_before) < pages.index(page_after):
        return True

    return False


def sum_middle_pages(updates: list[list[int]]) -> int:
    result: int = 0
    for pages in updates:
        result += pages[int((len(pages) - 1) / 2)]
    return result


def test_part_1():
    solution = sum_middle_pages(get_correctly_sorted_updates(*get_rules_and_updates(TEST_INPUT)))
    assert solution == 143


def solve_part_1():
    solution: int = sum_middle_pages(get_correctly_sorted_updates(*get_rules_and_updates(get_input(day=5))))
    assert solution == 5329


def test_part_2():
    solution: int = sum_middle_pages(get_incorrectly_sorted_updates(*get_rules_and_updates(TEST_INPUT)))
    assert solution == 123


def solve_part_2():
    solution: int = sum_middle_pages(get_incorrectly_sorted_updates(*get_rules_and_updates(get_input(day=5))))
    assert solution == 5833


if __name__ == "__main__":
    test_part_1()
    solve_part_1()
    test_part_2()
    solve_part_2()
