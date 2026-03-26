"""Root conftest.py — shared fixtures for all test suites."""

import http.server
import os
import socket
import threading
import pytest


# Path to the website source directory
SRC_DIR = os.path.join(os.path.dirname(__file__), "src")


class QuietHTTPHandler(http.server.SimpleHTTPRequestHandler):
    """Serves files from SRC_DIR without logging to stdout."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SRC_DIR, **kwargs)

    def log_message(self, format, *args):
        pass  # suppress request logs during tests


def _find_free_port():
    """Find a free port by letting the OS assign one."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", 0))
        return s.getsockname()[1]


class ReusableTCPServer(http.server.HTTPServer):
    """HTTP server that allows address reuse."""

    allow_reuse_address = True


@pytest.fixture(scope="session")
def base_url():
    """Start a local HTTP server on a dynamic port and return its base URL."""
    port = _find_free_port()
    server = ReusableTCPServer(("localhost", port), QuietHTTPHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://localhost:{port}"
    server.shutdown()


@pytest.fixture(scope="function")
def home_page(page, base_url):
    """Navigate to the home page and wait for load."""
    page.goto(base_url)
    page.wait_for_load_state("domcontentloaded")
    return page
