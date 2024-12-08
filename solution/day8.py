import dataclasses
from itertools import combinations
from typing import Optional

from input.manager import get_input

TEST_INPUT: str = (
    "............\n........0...\n.....0......\n.......0....\n....0.......\n......A.....\n............\n............\n........A...\n.........A..\n............\n............"
)

FREE_SPOT: str = "."


@dataclasses.dataclass(frozen=True)
class Antenna:
    x: int
    y: int
    char: str

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def __hash__(self):
        return hash((self.x, self.y, self.char))


@dataclasses.dataclass(frozen=True)
class AntiNode(Antenna):
    char: str = "#"
    antennas: Optional[list[Antenna]] = None

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def __hash__(self):
        return hash((self.x, self.y, self.char))


def find_anti_nodes(antenna: Antenna, other_antenna: Antenna, x_max: int, y_max: int) -> list[AntiNode]:
    if antenna == other_antenna:
        return []
    x1 = antenna.x
    y1 = antenna.y

    x2 = other_antenna.x
    y2 = other_antenna.y

    dx = x2 - x1
    dy = y2 - y1

    anti_nodes = []
    if 0 <= x1 - dx < x_max and 0 <= y1 - dy < y_max:
        anti_nodes.append(AntiNode(antennas=[antenna, other_antenna], x=x1 - dx, y=y1 - dy))
    if 0 <= x2 + dx < x_max and 0 <= y2 + dy < y_max:
        anti_nodes.append(AntiNode(antennas=[antenna, other_antenna], x=x2 + dx, y=y2 + dy))

    return anti_nodes


def count_anti_nodes(data: str, check_harmonics: bool = False) -> int:
    matrix = [list(row) for row in data.splitlines()]
    x_max = len(matrix)
    y_max = len(matrix[0])

    antennas: list[Antenna] = [
        Antenna(x=x, y=y, char=matrix[x][y]) for x in range(x_max) for y in range(y_max) if matrix[x][y] != FREE_SPOT
    ]

    nodes = set()
    for antenna in antennas:
        same_frequency_antennas = [other_antenna for other_antenna in antennas if (other_antenna.char == antenna.char)]
        for other_antenna in same_frequency_antennas:
            nodes.update([anti_node for anti_node in find_anti_nodes(antenna, other_antenna, x_max, y_max)])

        # Find antennas that have at least one other antenna
        if len(same_frequency_antennas) > 1 and check_harmonics:
            # Loop over all antenna combinations
            antenna_pairs = list(combinations(same_frequency_antennas, 2))
            for pair in antenna_pairs:
                antenna = pair[0]
                other_antenna = pair[1]
                nodes.update([node for node in find_anti_nodes_with_harmonics(antenna, other_antenna, x_max, y_max)])
                nodes.add(AntiNode(x=antenna.x, y=antenna.y, char="#", antennas=[antenna, other_antenna]))
                nodes.add(AntiNode(x=other_antenna.x, y=other_antenna.y, char="#", antennas=[antenna, other_antenna]))

    return len(nodes)


def find_anti_nodes_with_harmonics(
    antenna: Antenna,
    other_antenna: Antenna,
    x_max: int,
    y_max: int,
) -> list[AntiNode]:
    if antenna == other_antenna:
        return []
    x1 = antenna.x
    y1 = antenna.y

    x2 = other_antenna.x
    y2 = other_antenna.y

    dx = x2 - x1
    dy = y2 - y1

    anti_nodes = []

    offset_x = dx
    offset_y = dy

    has_added_node = True
    while has_added_node:
        has_added_node = False
        if 0 <= x1 - dx < x_max and 0 <= y1 - dy < y_max:
            has_added_node = True
            anti_nodes.append(AntiNode(antennas=[antenna, other_antenna], x=x1 - dx, y=y1 - dy, char="#"))
        if 0 <= x2 + dx < x_max and 0 <= y2 + dy < y_max:
            has_added_node = True
            anti_nodes.append(AntiNode(antennas=[antenna, other_antenna], x=x2 + dx, y=y2 + dy, char="#"))
        dx += offset_x
        dy += offset_y
    return anti_nodes


def test_part_1() -> None:
    assert count_anti_nodes(TEST_INPUT) == 14


def solve_part_1() -> None:
    assert count_anti_nodes(get_input(day=8)) == 259


def test_part_2() -> None:
    assert count_anti_nodes(TEST_INPUT, check_harmonics=True) == 34


def solve_part_2() -> None:
    assert count_anti_nodes(get_input(day=8), check_harmonics=True) == 927


if __name__ == "__main__":
    test_part_1()
    solve_part_1()
    test_part_2()
    solve_part_2()
