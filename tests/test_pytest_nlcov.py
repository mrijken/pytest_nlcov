def test_options(pytester):
    config = pytester.parseconfig("")
    assert config.option.nlcov_revision == "master"
    assert config.option.nlcov_fail_under is None

    config = pytester.parseconfig("--nlcov-revision=main")
    assert config.option.nlcov_revision == "main"
    assert config.option.nlcov_fail_under is None

    config = pytester.parseconfig("--nlcov-revision=main", "--nlcov-fail-under=0.7")
    assert config.option.nlcov_revision == "main"
    assert config.option.nlcov_fail_under == 0.7
