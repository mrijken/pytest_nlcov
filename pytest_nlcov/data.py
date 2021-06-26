import collections
import dataclasses
import pathlib
from typing import Dict
from typing import List
from typing import Optional


@dataclasses.dataclass
class Line:
    is_empty: Optional[bool] = None
    is_executed: Optional[bool] = None
    is_executable: Optional[bool] = None
    multilines: Optional[List[int]] = None  # all lines which belong to this starting line of a multiline statement


Lines = Dict[int, Line]
LinesPerFile = Dict[pathlib.Path, Lines]


def lines_per_file_factory():
    return collections.defaultdict(lambda: collections.defaultdict(Line))
