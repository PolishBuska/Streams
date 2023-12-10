from contextlib import ExitStack

import pytest

from app.main import app as actual_app

@pytest.fixture(autouse=True)
def app():
    with ExitStack():
        yield actual_app