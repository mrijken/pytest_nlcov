from importlib import reload

import pytest_nlcov
import pytest_nlcov.cov
import pytest_nlcov.data
import pytest_nlcov.format
import pytest_nlcov.git

pytest_plugins = "pytester"


# NOTE: Ensure modules are reloaded when coverage.py is looking.
#       This means we want to avoid importing module members when
#       using these modules, to ensure they get reloaded as well.
reload(pytest_nlcov)
reload(pytest_nlcov.cov)
reload(pytest_nlcov.data)
reload(pytest_nlcov.format)
reload(pytest_nlcov.git)
