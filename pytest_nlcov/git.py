import pathlib
from io import StringIO
from typing import Optional

import git
from unidiff import PatchSet

from .data import LinesPerFile
from .data import lines_per_file_factory


def get_diff(revision: str):
    return git.Repo(".").git.diff(revision, ignore_blank_lines=True, ignore_space_at_eol=True)


def get_new_lines_per_file(revision: str, glob: Optional[str] = None) -> LinesPerFile:
    """
    Get all lines which are new according to git.
    """
    uni_diff_text = get_diff(revision)

    lines_per_file = lines_per_file_factory()

    for patched_file in PatchSet(StringIO(uni_diff_text)):
        file_path = pathlib.Path(patched_file.path).resolve()
        if glob and not file_path.match(glob):
            continue
        for hunk in patched_file:
            for hunk_line in hunk:
                if hunk_line.target_line_no is None or not hunk_line.is_added:
                    continue
                line = lines_per_file[file_path][hunk_line.target_line_no]
                line.is_empty = hunk_line.value.strip() == ""

    return lines_per_file
