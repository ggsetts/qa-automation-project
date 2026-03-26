"""Worker mock helpers — intercept fetch calls to the Worker URL in E2E tests."""

import json

WORKER_URL = "https://contact-form.acmedist.workers.dev"


def mock_worker_success(page):
    """Route all requests to the Worker URL to return a 200 success response."""
    page.route(
        f"{WORKER_URL}**",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({"success": True}),
        ),
    )


def mock_worker_failure(page, status=500, error_message="Internal error"):
    """Route all requests to the Worker URL to return an error response."""
    page.route(
        f"{WORKER_URL}**",
        lambda route: route.fulfill(
            status=status,
            content_type="application/json",
            body=json.dumps({"error": error_message}),
        ),
    )


def mock_worker_network_error(page):
    """Abort all requests to the Worker URL to simulate a network failure."""
    page.route(
        f"{WORKER_URL}**",
        lambda route: route.abort("connectionrefused"),
    )
