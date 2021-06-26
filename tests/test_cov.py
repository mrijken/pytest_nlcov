from typing import Dict
from typing import List

from pytest_nlcov import cov
from pytest_nlcov.data import lines_per_file_factory


def test_mark_coveraged_lines_per_file(mocker):
    mocker.patch(
        "pytest_nlcov.cov.get_coverage_data",
        lambda: {"test.py": [1, 2, 3, 4, 5, 10, 11], "cov.py": [1, 2, 3]},
    )
    lines_per_file = lines_per_file_factory()
    lines_per_file["test.py"][1].is_empty = False
    lines_per_file["test.py"][2].is_empty = False
    lines_per_file["test.py"][3].is_empty = False
    lines_per_file["test.py"][10].is_empty = False

    cov.mark_coveraged_lines_per_file(lines_per_file)
    assert list(lines_per_file.keys()) == ["test.py"]
    assert list(lines_per_file["test.py"]) == [1, 2, 3, 10]
    assert [i.is_executed for _, i in lines_per_file["test.py"].items()] == [True, True, True, True]


class MockPythonParser:
    def __init__(self, statements: List[int], first_lines: Dict[int, int]):
        self.statements = statements
        self.first_lines = first_lines

    def first_line(self, line):
        return self.first_lines.get(line, line)


def test_mark_executable_lines_per_file(mocker):
    mocker.patch(
        "pytest_nlcov.cov.get_python_parser",
        lambda _: MockPythonParser([2, 3, 9], {10: 9}),
    )
    lines_per_file = lines_per_file_factory()
    lines_per_file["test.py"][1].is_empty = False
    lines_per_file["test.py"][2].is_empty = False
    lines_per_file["test.py"][3].is_empty = False
    lines_per_file["test.py"][10].is_empty = False

    cov.mark_executable_lines_per_file(lines_per_file)
    assert list(lines_per_file.keys()) == ["test.py"]
    assert list(lines_per_file["test.py"]) == [1, 2, 3, 10, 9]
    assert [line_no for line_no, i in lines_per_file["test.py"].items() if i.is_executable] == [
        2,
        3,
        10,
        9,
    ]
