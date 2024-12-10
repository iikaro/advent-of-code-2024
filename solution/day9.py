from input.manager import get_input
from solution.utils import print_solution

TEST_INPUT = "2333133121414131402"
SPACE_CHAR = "."


def reorganize_disk(data: str) -> list[str]:
    disk_map = list(data)
    new_disk_map = []
    length = len(disk_map)
    i = 0
    k = 0
    while i < length:
        j = i
        if i % 2 == 0:
            new_disk_map += int(disk_map[i]) * [str(k)]
            if j + 1 < length:
                while disk_map[j + 1] == disk_map[i]:
                    j += 1
            k += 1
        else:
            new_disk_map += int(disk_map[i]) * [SPACE_CHAR]
            while disk_map[j + 1] == disk_map[i]:
                j += 1
        i += 1
    return new_disk_map


def sort_disk(disk_map: str) -> list[str]:
    reversed_disk_map = list(reversed(disk_map))
    i = 0
    length = len(disk_map)
    while i < len(disk_map):
        if len(reversed_disk_map) == 0:
            break
        if disk_map[i] == SPACE_CHAR:
            if reversed_disk_map[0] == SPACE_CHAR:
                reversed_disk_map.pop(0)
                i -= 1
            else:
                disk_map[i] = reversed_disk_map[0]
                disk_map[length - 1 - disk_map[::-1].index(reversed_disk_map[0])] = SPACE_CHAR
                reversed_disk_map.pop(0)
        i += 1
    return disk_map


def sort_disk_by_blocks(disk_map: str) -> list[str]:
    reversed_disk_map = list(reversed(disk_map))
    i = 0
    length = len(disk_map)
    new_start_numbers = 0

    index = 0
    while i < length:
        # Find number slot to be moved
        while reversed_disk_map[index] == SPACE_CHAR:
            index +=1
        current_char = reversed_disk_map[index]
        start_numbers = new_start_numbers
        end_numbers = new_start_numbers
        if reversed_disk_map[index] != SPACE_CHAR:
            while reversed_disk_map[0] != current_char:
                start_numbers += 1
                end_numbers = start_numbers
            while reversed_disk_map[end_numbers] == current_char:
                end_numbers += 1
        number_slot_length = end_numbers - start_numbers
        number_slot = reversed_disk_map[start_numbers:end_numbers]
        print(f"Found number slot from {start_numbers} to {end_numbers}, {number_slot}")

        # Find space slot, from the beginning of the array, that may fit the number
        start_spaces = 0
        end_spaces = 0
        found_spaces = False
        while disk_map[start_spaces] != SPACE_CHAR and start_spaces < len(disk_map):
            start_spaces += 1
            end_spaces = start_spaces
            while disk_map[end_spaces] == SPACE_CHAR:
                end_spaces += 1
            space_slot_length = end_spaces - start_spaces
            if space_slot_length >= number_slot_length:
                found_spaces = True
                break
        space_slot = disk_map[start_spaces:end_spaces]
        print(f"Found space slot from {start_spaces} to {end_spaces}, {space_slot}")

        # Replace slot of "." by number slot
        has_replaced_number = False
        if found_spaces:
            has_replaced_number = True
            disk_map[start_spaces : start_spaces + number_slot_length] = reversed_disk_map[start_numbers:end_numbers]
            if number_slot_length > 0:
                count = 0
                while count < number_slot_length:
                    disk_map[length - 1 - disk_map[::-1].index(reversed_disk_map[0])] = SPACE_CHAR
                    count += 1
        if not has_replaced_number:
            reversed_disk_map += reversed_disk_map[start_numbers:end_numbers]
            new_start_numbers = start_numbers + number_slot_length
        else:
            new_start_numbers = 0
        reversed_disk_map = reversed_disk_map[end_numbers:]
        print("".join(reversed_disk_map))
        print("".join(disk_map))


    return disk_map


def get_sum(disk_map: list[str]) -> int:
    sum = 0
    for i, char in enumerate(disk_map):
        if char != SPACE_CHAR:
            sum += i * int(char)
    return sum


def solve(data: str) -> int:
    disk_map = reorganize_disk(data)
    sorted_disk_map = sort_disk(disk_map)
    solution = get_sum(sorted_disk_map)
    return solution


def test_part_1() -> None:
    data = TEST_INPUT
    disk_map = reorganize_disk(data)
    assert "".join(disk_map) == "00...111...2...333.44.5555.6666.777.888899"
    sorted_disk_map = sort_disk(disk_map)
    assert "".join(sorted_disk_map) == "0099811188827773336446555566.............."
    solution = get_sum(sorted_disk_map)
    assert solution == 1928


def test_part_2() -> None:
    data = TEST_INPUT
    disk_map = reorganize_disk(data)
    assert "".join(disk_map) == "00...111...2...333.44.5555.6666.777.888899"
    sorted_disk_map = sort_disk_by_blocks(disk_map)
    assert "".join(sorted_disk_map) == "00992111777.44.333....5555.6666.....8888.."
    solution = get_sum(sorted_disk_map)
    assert solution == 2858


def solve_part_1() -> None:
    data = get_input(day=9)
    disk_map = reorganize_disk(data)
    sorted_disk_map = sort_disk(disk_map)
    solution = get_sum(sorted_disk_map)
    print_solution(solution)


def solve_part_2() -> None:
    data = get_input(day=9)
    disk_map = reorganize_disk(data)
    sorted_disk_map = sort_disk_by_blocks(disk_map)
    solution = get_sum(sorted_disk_map)
    print_solution(solution)


if __name__ == "__main__":
    test_part_1()
    # solve_part_1()
    test_part_2()
    solve_part_2()
