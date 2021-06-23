from importlib import reload

import pytest

import pytest_nlcov

pytest_plugins = "pytester"


class DummyReporter:
    def __init__(self):
        self.lines = []

    def line(self, text=""):
        self.lines.append(text)

    def write_line(self, text="", **_):
        self.line(text)

    def section(self, title):
        self.line(f"###{title}###")

    def flush(self):
        self.lines = []

    @property
    def text(self):
        return "\n".join(self.lines)


@pytest.fixture
def dummy_reporter():
    return DummyReporter()


class DummyCoverage:
    def xml_report(self, outfile):
        with open(outfile, "w") as fp:
            fp.write("<dummy_report/>")


@pytest.fixture
def dummy_cov():
    return DummyCoverage()


# NOTE: Ensure modules are reloaded when coverage.py is looking.
#       This means we want to avoid importing module members when
#       using these modules, to ensure they get reloaded as well.
reload(pytest_nlcov)
