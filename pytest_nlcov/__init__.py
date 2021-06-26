import pathlib

import pytest
import typer

from .cov import mark_coveraged_lines_per_file
from .cov import mark_executable_lines_per_file
from .format import format_lines
from .git import get_new_lines_per_file


def make_relative(path: pathlib.Path) -> str:
    return str(path.relative_to(str(pathlib.Path(".").resolve())))


def nl_cov(revision: str = "master") -> float:
    """
    Get the coverage for new lines only.
    """
    typer.echo("New Line Coverage")
    typer.echo("")

    new_lines_per_file = get_new_lines_per_file(revision, glob="*.py")

    mark_executable_lines_per_file(new_lines_per_file)
    mark_coveraged_lines_per_file(new_lines_per_file)

    # Prepare the formatting strings, header, and column sorting.
    max_name = max([len(make_relative(p)) for p in new_lines_per_file] + [5])
    fmt_name = "%%- %ds  " % max_name
    fmt_skip_covered = "\n%s file%s skipped due to complete coverage."
    fmt_skip_empty = "\n%s empty file%s skipped."

    header = (fmt_name % "Name") + " Lines   Miss"
    fmt_coverage = fmt_name + "%6d %6d"

    header += "%*s" % (9, "Cover")
    fmt_coverage += " %%%ds" % (8,)

    header += "   Missing"
    fmt_coverage += "   %s"

    rule = "-" * len(header)

    # Write the header
    typer.echo(header)
    typer.echo(rule)

    total_num_newlines = 0
    total_num_covered = 0
    for (p, new_lines) in new_lines_per_file.items():
        num_newlines = len(
            [lineno for lineno, line in new_lines.items() if line.is_empty is False and line.is_executable is True]
        )

        if num_newlines == 0:
            continue

        num_covered = len(
            [
                lineno
                for lineno, line in new_lines.items()
                if line.is_executed is True and line.is_empty is False and line.is_executable is True
            ]
        )
        total_num_newlines += num_newlines
        total_num_covered += num_covered

        num_uncovered = num_newlines - num_covered

        args = (
            make_relative(p),
            num_newlines,
            num_uncovered,
            f"{num_covered / num_newlines:.0%}",
            format_lines(
                [
                    lineno
                    for lineno, line in new_lines.items()
                    if line.is_executed is not True and line.is_empty is False and line.is_executable is True
                ]
            ),
        )

        text = fmt_coverage % args

        typer.echo(text)

    # Write a TOTAL line if we had at least one file.
    if total_num_newlines > 0:
        typer.echo(rule)
        args = (
            "TOTAL",
            total_num_newlines,
            total_num_newlines - total_num_covered,
            f"{total_num_covered / total_num_newlines:.0%}",
            "",
        )

        typer.echo(fmt_coverage % args)

    return total_num_covered / total_num_newlines if total_num_newlines else 1


def cli():
    typer.run(nl_cov)


def validate_fail_under(num_str):
    try:
        return int(num_str)
    except ValueError:
        return float(num_str)


def pytest_addoption(parser):
    group = parser.getgroup("coverage for new lines")
    group.addoption(
        "--nlcov-revision",
        action="store",
        default="master",
        dest="nlcov_revision",
        help="Revision to determine the added lines",
    )
    group.addoption(
        "--nlcov-fail-under",
        action="store",
        type=validate_fail_under,
        help="Fail if the total coverage is less",
    )


class NLCovPlugin:
    @pytest.mark.trylast
    def pytest_terminal_summary(self, terminalreporter, config):
        cov_plugin = config.pluginmanager.get_plugin("_cov")
        if cov_plugin.cov_controller is None:
            terminalreporter.write_line("No _cov plugin available")
            return

        if cov_plugin.cov_total is None:
            terminalreporter.write_line("cov_total is None")
            return

        cov = cov_plugin.cov_controller.cov
        if cov is None:
            terminalreporter.write_line("Cov is None")
            return

        coverage = nl_cov(config.option.nlcov_revision)

        if config.option.cov_fail_under is not None and config.option.cov_fail_under > 0:
            failed = coverage < config.option.cov_fail_under
            terminalreporter.write(
                f'{"FAIL " if failed else ""}Required test coverage of {config.option.cov_fail_under}% {"not reached" if failed else "reached"}. '
                f"Total coverage: {coverage:.2f}%\n",
                **({"red": True, "bold": True} if failed else {"green": True}),
            )


def pytest_configure(config):  # pragma: no cover
    if not config.pluginmanager.has_plugin("_cov"):
        typer.echo("nlcov is installed, but pytest-cov is not installed, so nlcov will not be executed.")
        return
    config.pluginmanager.register(NLCovPlugin())
