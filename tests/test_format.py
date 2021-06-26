from pytest_nlcov.format import format_lines


def test_format_lines():
    assert format_lines([1, 2, 3, 4, 6, 8, 9, 10]) == "1-4, 6, 8-10"
    assert format_lines([]) == ""
