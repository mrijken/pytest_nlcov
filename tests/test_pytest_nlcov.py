import pytest

from pytest import UsageError
from pytest_nlcov import NLCovPlugin


def test_options(pytester, no_gitpython):
    config = pytester.parseconfig("")
    assert config.option.nlcov_revision is None

    config = pytester.parseconfig("--nlcov_revision master")
    assert config.option.nlcov_revision == "master"
