import pathlib

from coverage import CoverageData
from coverage import parser

from .data import LinesPerFile
from .data import lines_per_file_factory


def get_coveraged_lines_per_file() -> LinesPerFile:
    coverage_data = CoverageData()
    coverage_data.read()

    lines_per_file: LinesPerFile = lines_per_file_factory()
    for measured_file in coverage_data.measured_files():
        for coveraged_lineno in coverage_data.lines(measured_file):
            lines_per_file[pathlib.Path(measured_file).resolve()][coveraged_lineno].is_executed = True

        parsed_file = parser.PythonParser(filename=measured_file)
        parsed_file.parse_source()
        for executable_lineno in parsed_file.statements:
            lines_per_file[pathlib.Path(measured_file).resolve()][executable_lineno].is_executable = True

    return lines_per_file
