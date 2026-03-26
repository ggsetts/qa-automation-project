# Test Strategy

## Tool Selection

### Why Playwright (Python)

- **Multi-browser:** Test on Chromium, Firefox, and WebKit from one framework
- **Built-in mobile emulation:** Viewport resizing, touch simulation
- **Network interception:** Mock API responses without external tools
- **Screenshot comparison:** Native `to_have_screenshot()` for visual regression
- **Python ecosystem:** pytest integration, familiar to most QA engineers

### Why Not Cypress

- Single browser engine (Chromium-based only)
- No native mobile emulation
- JavaScript-only — less portable across QA teams

### Why Not Selenium

- Slower execution, heavier setup
- Less modern API, more boilerplate
- Playwright is the industry direction for new projects

## Test Pyramid

```
         /  Visual (6)  \        ← Slow, catch pixel drift
        /  E2E (34)      \       ← User journey simulation
       / Responsive (11)   \     ← Layout verification
      / Accessibility (8)    \   ← WCAG compliance
     / API Contract (20)      \  ← Schema + behavior
    /  Smoke (10)              \ ← Fast CI gate
```

## Flakiness Mitigation

1. **Dynamic port allocation:** No hardcoded server ports — prevents conflicts
2. **domcontentloaded over networkidle:** External scripts (Turnstile) keep connections open; we don't wait for them
3. **Explicit waits:** `wait_for_timeout` after scroll/animation actions
4. **Mocked external dependencies:** Worker URL intercepted — no real network calls in E2E
5. **Independent test fixtures:** Each test gets a fresh page via pytest-playwright

## Risk-Based Prioritization

The contact form receives the most coverage because:
- It is the only user-to-business conversion mechanism
- It involves external service integration (Worker + Formspree)
- It has the most interactive states (validation, loading, success, error)
- A broken form directly impacts business revenue
