import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities as _activities


_ORIG_ACTIVITIES = copy.deepcopy(_activities)


@pytest.fixture
def client():
    tc = TestClient(app)

    # Some versions of TestClient/httpx expect 'follow_redirects' while tests
    # may call 'allow_redirects'. Provide a thin wrapper to accept
    # 'allow_redirects' and map it to 'follow_redirects' to avoid TypeError in tests.
    original_get = tc.get

    def get_with_allow_redirects(path, *args, **kwargs):
        if 'allow_redirects' in kwargs:
            kwargs['follow_redirects'] = kwargs.pop('allow_redirects')
        return original_get(path, *args, **kwargs)

    tc.get = get_with_allow_redirects
    return tc


@pytest.fixture(autouse=True)
def reset_activities():
    # Reset the in-memory activities dict before each test for isolation
    _activities.clear()
    _activities.update(copy.deepcopy(_ORIG_ACTIVITIES))
    yield
