import pathlib
from io import StringIO

import git
from unidiff import PatchSet

from .data import LinesPerFile
from .data import lines_per_file_factory


def get_new_lines_per_file(revision: str) -> LinesPerFile:
    uni_diff_text = git.Repo(".").git.diff(revision, ignore_blank_lines=True, ignore_space_at_eol=True)

    lines_per_file = lines_per_file_factory()

    for patched_file in PatchSet(StringIO(uni_diff_text)):
        for hunk in patched_file:
            for hunk_line in hunk:
                line = lines_per_file[pathlib.Path(patched_file.path).resolve()][hunk_line.target_line_no]
                line.is_new = hunk_line.is_added
                line.is_empty = hunk_line.value.strip() == ""

    # Note: this function does not (yet) mark the whole statement as new, but just a line
    # So in case of a multiline statement, the statement is only marked as new as the first
    # of the statement is matched

    return lines_per_file
