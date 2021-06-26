# pytest_nlcov

With `pytest_nlcov` you can check the test coverage of new lines only. It will
check git for added and modified lines and will compute the coverage
just for those lines

## Installation

```sh
pip install pytest_nlcov
```

Note: `pytest_cov` is required and will be automatically installed when it 
is not installed yet.

## Usage with pytest

When `pytest_nlcov` is installed, it will be discovered by pytest and executed as last step to
show you the test coverage of new lines.

```sh
pytest
```

Two option can be given:

- revision
- fail threshold

### Revision

Default, the new lines are based on the git diff with master. You can specify other revisions.

```sh
pytest --nlcov-revision main
```

### Fail Threshold

Optionally you can add a threshold to fail the tests when the coverage is below the threshold.

```sh
pytest --nlcov-fail-under 0.6
```

## Usage without pytest

`pytest_nlcov` can be run without pytest. Therefor you have to run `coverage` first, because `pytest_nlcov`
needs its coverage data.

```sh
coverage
nlcov
```

Optionally a revision can be given

```sh
nlcov main
```
