"""Integration tests for error simulation API routes."""

from typing import Any

from fastapi.testclient import TestClient


def _assert_error_shape(body: dict[str, Any], expected_code: str) -> None:
    """Assert the standard error response structure."""
    assert "error" in body
    error = body["error"]
    assert error["code"] == expected_code
    assert "message" in error
    assert isinstance(error["message"], str)


class TestNotFoundError:
    """Integration tests for 404 NotFoundError route."""

    def test_status_code(self, client: TestClient) -> None:
        """Verify the route returns a 404 status code."""
        response = client.get("/error/not-found")
        assert response.status_code == 404

    def test_error_code(self, client: TestClient) -> None:
        """Verify the error code in the response body is correct."""
        body = client.get("/error/not-found").json()
        _assert_error_shape(body, "NOT_FOUND")

    def test_details_present(self, client: TestClient) -> None:
        """Verify the error details include the expected resource information."""
        body = client.get("/error/not-found").json()
        assert "details" in body["error"]
        assert body["error"]["details"]["resource"] == "Item"


class TestAuthenticationError:
    """Integration tests for 401 AuthenticationError route."""

    def test_status_code(self, client: TestClient) -> None:
        """Verify the route returns a 401 status code."""
        response = client.get("/error/authentication")
        assert response.status_code == 401

    def test_error_code(self, client: TestClient) -> None:
        """Verify the error code in the response body is correct."""
        body = client.get("/error/authentication").json()
        _assert_error_shape(body, "AUTHENTICATION_FAILED")


class TestAuthorizationError:
    """Integration tests for 403 AuthorizationError route."""

    def test_status_code(self, client: TestClient) -> None:
        """Verify the route returns a 403 status code."""
        response = client.get("/error/authorization")
        assert response.status_code == 403

    def test_error_code(self, client: TestClient) -> None:
        """Verify the error code in the response body is correct."""
        body = client.get("/error/authorization").json()
        _assert_error_shape(body, "PERMISSION_DENIED")

    def test_details_present(self, client: TestClient) -> None:
        """Verify the error details include the expected action and resource information."""
        body = client.get("/error/authorization").json()
        assert body["error"]["details"]["action"] == "delete"
        assert body["error"]["details"]["resource"] == "Item"


class TestValidationError:
    """Integration tests for 422 validation error route."""

    def test_valid_payload_returns_200(self, client: TestClient) -> None:
        """Verify that a valid request payload returns a 200 status code."""
        response = client.post(
            "/error/validation/item",
            json={"name": "Widget", "quantity": 5},
        )
        assert response.status_code == 200

    def test_missing_required_field_returns_422(self, client: TestClient) -> None:
        """Verify that omitting required fields results in a 422 status code."""
        response = client.post("/error/validation/item", json={})
        assert response.status_code == 422

    def test_invalid_quantity_returns_422(self, client: TestClient) -> None:
        """Verify that an invalid quantity value results in a 422 status code."""
        response = client.post(
            "/error/validation/item",
            json={"name": "Widget", "quantity": 0},
        )
        assert response.status_code == 422

    def test_empty_name_returns_422(self, client: TestClient) -> None:
        """Verify that an empty name value results in a 422 status code."""
        response = client.post(
            "/error/validation/item",
            json={"name": "", "quantity": 1},
        )
        assert response.status_code == 422

    def test_422_error_shape(self, client: TestClient) -> None:
        """Verify that the error response for validation errors follows the expected structure."""
        body = client.post("/error/validation/item", json={}).json()
        _assert_error_shape(body, "INVALID_INPUT")

    def test_validation_details_contain_errors_list(self, client: TestClient) -> None:
        """Verify that the validation error details contain a list of errors."""
        body = client.post("/error/validation/item", json={}).json()
        assert "errors" in body["error"]["details"]
        assert isinstance(body["error"]["details"]["errors"], list)

    def test_validation_error_item_has_field_and_message(self, client: TestClient) -> None:
        """Verify that each validation error item contains a field and message."""
        body = client.post("/error/validation/item", json={}).json()
        first_error = body["error"]["details"]["errors"][0]
        assert "field" in first_error
        assert "message" in first_error


class TestConflictError:
    """Integration tests for 409 ConflictError route."""

    def test_status_code(self, client: TestClient) -> None:
        """Verify the route returns a 409 status code."""
        response = client.post("/error/conflict")
        assert response.status_code == 409

    def test_error_code(self, client: TestClient) -> None:
        """Verify the error code in the response."""
        body = client.post("/error/conflict").json()
        _assert_error_shape(body, "RESOURCE_CONFLICT")

    def test_details_present(self, client: TestClient) -> None:
        """Verify that the error details include the expected resource information."""
        body = client.post("/error/conflict").json()
        assert body["error"]["details"]["resource"] == "Item"


class TestExternalServiceError:
    """Integration tests for 503 ExternalServiceError route."""

    def test_status_code(self, client: TestClient) -> None:
        """Verify the route returns a 503 status code."""
        response = client.post("/error/external-service")
        assert response.status_code == 503

    def test_error_code(self, client: TestClient) -> None:
        """Verify the error code in the response."""
        body = client.post("/error/external-service").json()
        _assert_error_shape(body, "SERVICE_UNAVAILABLE")

    def test_details_present(self, client: TestClient) -> None:
        """Verify that the error details include the expected service information."""
        body = client.post("/error/external-service").json()
        assert body["error"]["details"]["service"] == "PaymentGateway"


class TestHTTPError:
    """Integration tests for generic HTTPException route."""

    def test_status_code(self, client: TestClient) -> None:
        """Verify the route returns a 400 status code."""
        response = client.get("/error/http")
        assert response.status_code == 400

    def test_error_code(self, client: TestClient) -> None:
        """Verify the error code in the response."""
        body = client.get("/error/http").json()
        _assert_error_shape(body, "BAD_REQUEST")


class TestUnhandledError:
    """Integration tests for unhandled exception catch-all route."""

    def test_status_code(self, client: TestClient) -> None:
        """Verify the route returns a 500 status code."""
        response = client.get("/error/unhandled")
        assert response.status_code == 500

    def test_error_code(self, client: TestClient) -> None:
        """Verify the error code in the response."""
        body = client.get("/error/unhandled").json()
        _assert_error_shape(body, "INTERNAL_ERROR")
