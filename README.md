# QA Portfolio — Automated Test Suite for E-Commerce Distribution Site

A comprehensive automated test suite demonstrating senior QA engineering skills, built for a static business website with a Cloudflare Worker backend.

## Test Suite Overview

| Suite | Tests | What It Validates |
|---|---|---|
| **Smoke** | 10 | Critical-path checks (page loads, sections exist, no JS errors) |
| **E2E** | 34 | Full user journeys (navigation, contact form, mobile menu, scroll) |
| **Responsive** | 11 | Grid layouts at desktop (1280px), tablet (768px), mobile (375px) |
| **Accessibility** | 8 | WCAG 2.1 AA via axe-core, keyboard nav, ARIA attributes |
| **API/Contract** | 20 | Worker behavior validation, response schema, Pydantic models |
| **Security** | 9 | CORS, XSS payloads, secret leakage, input limits |
| **Visual** | 6 | Pixel-level screenshot comparison (baseline-based) |
| **Total** | **98** | |

## Tech Stack

- **Python 3.9+** — Test language
- **pytest** — Test framework and runner
- **Playwright** — Browser automation (Chromium, Firefox, WebKit)
- **axe-core** — Accessibility scanning (WCAG 2.1 AA)
- **Pydantic** — API response schema validation
- **GitHub Actions** — CI/CD with cross-browser matrix

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install chromium

# Run all tests (excluding visual regression)
python -m pytest tests/ --ignore=tests/visual --ignore=tests/performance -v --browser chromium

# Run specific suites
python -m pytest tests/smoke/ -v --browser chromium       # Smoke tests
python -m pytest tests/e2e/ -v --browser chromium          # E2E tests
python -m pytest tests/responsive/ -v --browser chromium   # Responsive tests
python -m pytest tests/accessibility/ -v --browser chromium # Accessibility tests
python -m pytest tests/api/ -v --browser chromium          # API + security tests

# Run by marker
python -m pytest -m smoke -v --browser chromium
python -m pytest -m security -v --browser chromium
```

## Project Structure

```
qa-portfolio-website/
├── src/                        # Website under test
│   ├── index.html              # Single-page site (nav, hero, categories, contact form)
│   ├── styles.css              # Responsive CSS (breakpoints: 900px, 500px)
│   └── worker/                 # Cloudflare Worker backend
│       └── contact-form-worker.js
├── tests/
│   ├── e2e/                    # End-to-end user journey tests
│   ├── responsive/             # Breakpoint and layout tests
│   ├── accessibility/          # WCAG 2.1 AA compliance tests
│   ├── visual/                 # Screenshot regression tests
│   ├── api/                    # Worker contract, unit, and security tests
│   ├── smoke/                  # Fast CI gate tests
│   └── fixtures/               # Page Objects, test data, helpers
│       ├── pages/              # Page Object Models (base, home, contact, nav)
│       ├── test_data.py        # Centralized test data factory
│       └── helpers/            # Worker mocks, a11y helpers
├── docs/
│   ├── test-strategy.md        # Tool choices, test pyramid, flakiness mitigation
│   ├── bug-report-template.md  # Template + 2 real findings
│   └── test-case-examples.md   # Manual test cases for non-automatable scenarios
├── TEST_PLAN.md                # Formal test plan (IEEE 829 style)
├── .github/workflows/ci.yml   # CI pipeline with cross-browser matrix
├── conftest.py                 # Root fixtures (dynamic HTTP server, page setup)
├── pytest.ini                  # pytest config with test markers
└── requirements.txt            # Python dependencies
```

## Architecture Decisions

- **Page Object Model pattern** — Encapsulates page interactions for maintainability
- **Dynamic port allocation** — Prevents port conflicts in parallel/CI environments
- **Mocked external services** — Worker URL intercepted to avoid real API calls in tests
- **domcontentloaded over networkidle** — External Turnstile script keeps connections open
- **Pydantic for contract testing** — Typed schema validation with clear error messages

## Key Findings

Real issues discovered during test development:

1. **Missing skip-to-content link** (WCAG 2.4.1) — keyboard users must tab through all nav links before reaching content
2. **Turnstile widget accessibility** — third-party iframe may not meet color contrast ratios
3. **No server-side input sanitization** — Worker forwards form data as-is to Formspree (XSS payloads pass through)

See [docs/bug-report-template.md](docs/bug-report-template.md) for detailed write-ups.

## CI/CD Pipeline

The GitHub Actions pipeline runs on every push and PR:

1. **Smoke tests** — fast gate (fail-fast)
2. **E2E tests** — cross-browser matrix (Chromium, Firefox, WebKit)
3. **Responsive tests** — layout verification
4. **Accessibility tests** — WCAG compliance
5. **API tests** — contract and security validation
