import os

from local_env import ROOT

SOURCE = "input"


def get_input(day: int) -> list[str]:
    file_name: str = os.path.join(os.path.join(ROOT, SOURCE), "day" + str(day) + ".txt")
    return _read_lines_from_file(file_name)


def _read_lines_from_file(file_name: str) -> list[str]:
    with open(file_name, "r") as file:
        data = file.read().splitlines()
    return data
