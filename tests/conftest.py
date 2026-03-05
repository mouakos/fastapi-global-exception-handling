"""Shared fixtures for the test suite."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    """Return a test client for the FastAPI application."""
    return TestClient(app, raise_server_exceptions=False)
