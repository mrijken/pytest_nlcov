import pathlib
from typing import Dict, List
import typer
from io import StringIO
from coverage import CoverageData

import git
from unidiff import PatchSet
import pytest


def get_new_lines_per_file(revision: str) -> Dict[str, List[int]]:
    repository = git.Repo(".")

    uni_diff_text = repository.git.diff(revision, ignore_blank_lines=True, ignore_space_at_eol=True)

    new_lines_per_file: Dict[str, List[int]] = {}

    for patched_file in PatchSet(StringIO(uni_diff_text)):
        file_path = str(pathlib.Path(patched_file.path).absolute())
        new_lines = [
            line.source_line_no
            for hunk in patched_file
            for line in hunk
            if line.is_removed and line.value.strip() != ""
        ]
        new_lines_per_file[file_path] = new_lines

    return new_lines_per_file


def get_coveraged_lines_per_file() -> Dict[str, List[int]]:
    coverage_data = CoverageData()
    coverage_data.read()
    return {measured_file: coverage_data.lines(measured_file) for measured_file in coverage_data.measured_files()}


def nl_cov(revision: str) -> float:
    """
    Get the coverage for added lines only.
    """
    new_lines_per_file = get_new_lines_per_file(revision)

    coveraged_lines_per_file = get_coveraged_lines_per_file()
    print(coveraged_lines_per_file)

    coveraged_newlines_per_file: Dict[str, List[int]] = {}
    uncoveraged_newlines_per_file: Dict[str, List[int]] = {}
    for file_path, new_lines in new_lines_per_file.items():
        if not file_path.endswith(".py"):
            continue

        coveraged_lines = coveraged_lines_per_file.get(file_path, [])
        coveraged_newlines_per_file[file_path] = [i for i in new_lines if i in coveraged_lines]
        uncoveraged_newlines_per_file[file_path] = [i for i in new_lines if i not in coveraged_lines]

        typer.echo(f"File: {file_path}")
        typer.echo(
            f" coveraged new lines  : {len(coveraged_newlines_per_file[file_path])} ({coveraged_newlines_per_file[file_path]})"
        )
        typer.echo(
            f" uncoveraged new lines: {len(uncoveraged_newlines_per_file[file_path])} ({uncoveraged_newlines_per_file[file_path]})"
        )

    number_of_lines_coveraged = sum(len(i) for i in coveraged_newlines_per_file.values())
    number_of_lines_uncoveraged = sum(len(i) for i in uncoveraged_newlines_per_file.values())
    coverage_newlines = (
        number_of_lines_coveraged / (number_of_lines_coveraged + number_of_lines_uncoveraged)
        if (number_of_lines_coveraged + number_of_lines_uncoveraged) > 0
        else 1
    )
    typer.echo("")
    typer.echo("Total: ")
    typer.echo(f"  new lines   : {number_of_lines_uncoveraged + number_of_lines_coveraged}")
    typer.echo(f"  uncoveraged : {number_of_lines_uncoveraged}")
    typer.echo(f"  coveraged   : {number_of_lines_coveraged}")
    typer.echo(f"  coverage             : {coverage_newlines:.1%}")

    return coverage_newlines


def cli():
    typer.run(nl_cov)


def pytest_addoption(parser, pluginmanager):
    group = parser.getgroup("nlcov")
    group.addoption(
        "--nlcov",
        action="store_true",
        default=False,
        dest="nlcov",
        help="Enable nlcov",
    )
    group.addoption(
        "--nlcov_revision",
        action="store",
        default="master",
        dest="nlcov_revision",
        help="Revision to determine the added lines",
    )


class NLCovPlugin:
    @pytest.mark.trylast
    def pytest_nlcov(self, config):
        coverage = show_nl_cov(config.option.nlcov_revision)
        assert (
            not config.option.cov_fail_under or coverage > config.option.cov_fail_under
        ), "New line coverage is too low"


def pytest_configure(config):  # pragma: no cover
    # NOTE: if cov is missing we fail silently
    if config.option.nlcov and config.pluginmanager.has_plugin("_cov"):
        config.pluginmanager.register(NLCovPlugin())
