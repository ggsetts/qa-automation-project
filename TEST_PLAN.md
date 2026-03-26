# Test Plan — Acme Distribution Website

## 1. Introduction

This test plan covers the automated quality assurance for the Acme Distribution website, a static single-page business site with a Cloudflare Worker backend for contact form processing.

## 2. Test Items

- **Frontend:** Single-page HTML/CSS/JS site (index.html, styles.css)
- **Backend:** Cloudflare Worker contact form proxy (contact-form-worker.js)
- **Integrations:** Cloudflare Turnstile CAPTCHA, Formspree form delivery

## 3. Features to Test

| Feature | Priority | Approach |
|---|---|---|
| Navigation (links, scroll, mobile menu) | High | E2E automated |
| Contact form (validation, submission, states) | Critical | E2E automated |
| Responsive layout (3 breakpoints) | High | Automated viewport testing |
| Accessibility (WCAG 2.1 AA) | High | axe-core + manual keyboard |
| Visual consistency | Medium | Screenshot comparison |
| Worker API behavior | Critical | Contract + static analysis |
| Security (CORS, XSS, secrets) | High | Static analysis + runtime |

## 4. Features Not Tested

- Email delivery end-to-end (requires live Formspree integration)
- Cloudflare Turnstile widget behavior under rate limiting
- Real-device testing on physical iOS/Android devices
- DNS/CDN configuration and performance

## 5. Approach

**Automation-first, risk-based prioritization.** The contact form is the highest-risk feature (it is the site's primary conversion mechanism), so it receives the most test coverage.

**Test pyramid:**
- **Unit/Contract (20 tests):** Worker behavior validation, schema checking
- **Integration (11 tests):** Responsive breakpoints, accessibility scans
- **E2E (34 tests):** Full user journey simulation
- **Smoke (10 tests):** Fast critical-path subset for CI gating

## 6. Pass/Fail Criteria

- All smoke tests must pass before merging
- Zero critical accessibility violations
- All E2E tests pass on Chromium (Firefox/WebKit are advisory)
- No hardcoded secrets in source code
- All API contract schemas valid

## 7. Environment

- **Local:** Python 3.9+, Playwright browsers, http.server
- **CI:** GitHub Actions, Ubuntu latest, Python 3.11
- **Browsers:** Chromium (primary), Firefox, WebKit (matrix)

## 8. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Turnstile blocks test automation | Mock Turnstile tokens in E2E tests |
| Flaky scroll-based tests | Use explicit waits + viewport assertions |
| External font loading affects visual tests | Run visual tests after domcontentloaded |
| Port conflicts in parallel runs | Dynamic port allocation in conftest.py |
