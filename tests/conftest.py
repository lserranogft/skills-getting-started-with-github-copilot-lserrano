import copy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture()
def activity_store():
    """Restore the in-memory activity catalog after each test."""
    original_state = copy.deepcopy(app_module.activities)

    yield app_module.activities

    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original_state))


@pytest.fixture()
def client(activity_store):
    """Create a real TestClient for the FastAPI application."""
    with TestClient(app_module.app) as test_client:
        yield test_client
