import os

from local_env import ROOT

SOURCE = "input"


def get_input(day: int) -> str:
    file_name: str = os.path.join(os.path.join(ROOT, SOURCE), "day" + str(day) + ".txt")
    return _read_from_file(file_name)


def get_input_lines(day: int) -> list[str]:
    return get_input(day).splitlines()


def _read_from_file(file_name: str) -> str:
    with open(file_name, "r") as file:
        data = file.read()
    return data
