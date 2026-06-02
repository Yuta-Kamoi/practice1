import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities as _activities


_ORIG_ACTIVITIES = copy.deepcopy(_activities)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    # Reset the in-memory activities dict before each test for isolation
    _activities.clear()
    _activities.update(copy.deepcopy(_ORIG_ACTIVITIES))
    yield
