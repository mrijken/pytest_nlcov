import pathlib

from coverage import CoverageData
from coverage import parser

from .data import LinesPerFile


def get_coverage_data():
    coverage_data = CoverageData()
    coverage_data.read()

    return {
        pathlib.Path(measured_file).resolve(): coverage_data.lines(measured_file)
        for measured_file in coverage_data.measured_files()
    }


def mark_coveraged_lines_per_file(lines_per_file: LinesPerFile):
    """ """
    coverage_data = get_coverage_data()

    # remove first the files which have new lines but are not included in the coverage
    covered_files = set(coverage_data.keys())
    newline_files = set(lines_per_file.keys())
    not_covered_newline_files = newline_files - covered_files
    for file in not_covered_newline_files:
        del lines_per_file[file]

    for measured_file, coveraged_linenos in coverage_data.items():
        if measured_file not in lines_per_file:
            continue
        for coveraged_lineno in coveraged_linenos:
            if coveraged_lineno not in lines_per_file[measured_file]:
                continue
            lines_per_file[measured_file][coveraged_lineno].is_executed = True
            for subline in lines_per_file[measured_file][coveraged_lineno].multilines or []:
                lines_per_file[measured_file][subline].is_executed = True


def get_python_parser(file_path) -> parser.PythonParser:
    parsed_file = parser.PythonParser(filename=file_path)
    parsed_file.parse_source()

    return parsed_file


def mark_executable_lines_per_file(lines_per_file: LinesPerFile) -> LinesPerFile:
    """
    Mark the executable lines based on a Python parser.
    When a line is marked as new and it belongs to a multiline statement,
    the first line of that statement is added and marked as new too.
    """
    for file_path, lines in lines_per_file.items():
        parsed_file = get_python_parser(file_path)
        executable_linenos = parsed_file.statements
        for lineno, line in list(lines.items()):
            if lineno in executable_linenos:
                line.is_executable = True
            lineno_of_multiline_statement = parsed_file.first_line(lineno)
            if lineno_of_multiline_statement != lineno:
                lines[lineno].is_executable = lines[lineno_of_multiline_statement].is_executable = True
                multilines = lines[lineno_of_multiline_statement].multilines or []
                multilines.append(lineno)
                lines[lineno_of_multiline_statement].multilines = multilines
