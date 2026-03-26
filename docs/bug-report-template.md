# Bug Report Template

## Template

| Field | Value |
|---|---|
| **Title** | [Short description] |
| **Severity** | Critical / High / Medium / Low |
| **Component** | [Frontend / Backend / Accessibility / Performance] |
| **Environment** | [Browser, OS, viewport] |
| **Steps to Reproduce** | 1. ... 2. ... 3. ... |
| **Expected Result** | [What should happen] |
| **Actual Result** | [What actually happens] |
| **Screenshot/Evidence** | [Attach if applicable] |
| **Suggested Fix** | [Optional] |

---

## Real Finding: Missing Skip-to-Content Link

| Field | Value |
|---|---|
| **Title** | No skip-to-content link for keyboard/screen reader users |
| **Severity** | Medium |
| **Component** | Accessibility |
| **Environment** | All browsers, all viewports |
| **Steps to Reproduce** | 1. Open the website 2. Press Tab key 3. Observe the first focusable element |
| **Expected Result** | First Tab press should focus a "Skip to main content" link that allows users to bypass the navigation bar |
| **Actual Result** | First Tab press focuses the first nav link. Keyboard users must tab through all 4 nav links before reaching page content |
| **WCAG Reference** | WCAG 2.1 Success Criterion 2.4.1 (Bypass Blocks) — Level A |
| **Impact** | Screen reader and keyboard-only users must navigate through repetitive navigation on every page load |
| **Suggested Fix** | Add a visually-hidden skip link as the first element in `<body>`: `<a href="#about" class="skip-link">Skip to main content</a>` with CSS that makes it visible on focus |

---

## Real Finding: Turnstile Widget May Fail Color Contrast

| Field | Value |
|---|---|
| **Title** | Cloudflare Turnstile widget iframe may not meet WCAG color contrast ratios |
| **Severity** | Low |
| **Component** | Accessibility (third-party) |
| **Environment** | All browsers when Turnstile widget renders |
| **Steps to Reproduce** | 1. Navigate to Contact section 2. Run axe-core scan 3. Check color-contrast violations |
| **Expected Result** | All text meets 4.5:1 contrast ratio |
| **Actual Result** | Turnstile widget content is rendered in an iframe controlled by Cloudflare — contrast may not meet WCAG AA |
| **Impact** | Low — this is a third-party widget outside our control |
| **Suggested Fix** | Document as known limitation. Consider filing feedback with Cloudflare |
