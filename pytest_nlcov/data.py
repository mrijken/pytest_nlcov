import collections
import dataclasses
import pathlib
from typing import Dict
from typing import Optional


@dataclasses.dataclass
class Line:
    is_new: Optional[bool] = None
    is_empty: Optional[bool] = None
    is_executed: Optional[bool] = None
    is_executable: Optional[bool] = None


Lines = Dict[int, Line]
LinesPerFile = Dict[pathlib.Path, Lines]


def lines_per_file_factory():
    return collections.defaultdict(lambda: collections.defaultdict(Line))


def _merge_line(first, second):
    new = Line()
    for attr in ("is_new", "is_empty", "is_executed", "is_executable"):
        first_attr = getattr(first, attr)
        second_attr = getattr(second, attr)
        setattr(new, attr, first_attr if second_attr is None else second_attr)

    return new


def merge_lines(*merges: LinesPerFile) -> LinesPerFile:
    """
    Merge multiple LinesPerFile. Eventually all files and their lines will
    be part of the result with per attr the first value per `merges` which is not None.
    """
    lines_per_file = lines_per_file_factory()
    for merge in merges:
        for path, lines in merge.items():
            for lineno, line in lines.items():
                lines_per_file[path][lineno] = _merge_line(lines_per_file[path][lineno], line)

    return lines_per_file
