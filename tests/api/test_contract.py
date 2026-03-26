"""API contract tests — validate response schemas using Pydantic models."""

import pytest
from pydantic import BaseModel, ValidationError
from tests.fixtures.test_data import WORKER_SUCCESS_RESPONSE, WORKER_ERROR_RESPONSES


class SuccessResponse(BaseModel, extra="forbid"):
    """Expected schema for successful Worker responses."""
    success: bool


class ErrorResponse(BaseModel, extra="forbid"):
    """Expected schema for error Worker responses."""
    error: str


@pytest.mark.api
class TestResponseContracts:
    """Validate that Worker response payloads conform to expected schemas."""

    def test_success_response_schema(self):
        """Success response should match {success: bool} schema."""
        response = SuccessResponse(**WORKER_SUCCESS_RESPONSE)
        assert response.success is True

    def test_missing_token_error_schema(self):
        """Missing token error should match {error: str} schema."""
        response = ErrorResponse(**WORKER_ERROR_RESPONSES["missing_token"])
        assert response.error == "Missing Turnstile token"

    def test_invalid_token_error_schema(self):
        """Invalid token error should match {error: str} schema."""
        response = ErrorResponse(**WORKER_ERROR_RESPONSES["invalid_token"])
        assert response.error == "Turnstile verification failed"

    def test_method_not_allowed_error_schema(self):
        """Method not allowed error should match {error: str} schema."""
        response = ErrorResponse(**WORKER_ERROR_RESPONSES["method_not_allowed"])
        assert response.error == "Method not allowed"

    def test_form_service_error_schema(self):
        """Form service error should match {error: str} schema."""
        response = ErrorResponse(**WORKER_ERROR_RESPONSES["form_service_error"])
        assert response.error == "Form service error"

    def test_internal_error_schema(self):
        """Internal error should match {error: str} schema."""
        response = ErrorResponse(**WORKER_ERROR_RESPONSES["internal_error"])
        assert response.error == "Internal error"

    def test_success_response_rejects_extra_fields(self):
        """Success schema should reject unexpected fields in strict mode."""
        with pytest.raises(ValidationError):
            SuccessResponse(success=True, extra_field="unexpected")

    def test_error_response_rejects_missing_field(self):
        """Error schema should reject missing 'error' field."""
        with pytest.raises(ValidationError):
            ErrorResponse()
