# Manual Test Cases

These test cases cover scenarios that are difficult or impractical to automate.

## TC-001: Cross-Device Contact Form Submission

**Objective:** Verify the contact form works on real physical devices.

| Step | Action | Expected Result |
|---|---|---|
| 1 | Open site on iPhone Safari | Page loads, responsive layout |
| 2 | Tap hamburger menu | Menu opens smoothly |
| 3 | Tap "Contact" | Scrolls to contact section, menu closes |
| 4 | Fill all form fields | Keyboard appears, fields accept input |
| 5 | Complete Turnstile challenge | Widget shows success checkmark |
| 6 | Tap "Send Message" | Button shows "Sending...", then success message |

**Devices:** iPhone 14 (Safari), Samsung Galaxy S23 (Chrome), iPad Pro (Safari)

## TC-002: Email Delivery Verification

**Objective:** Verify that submitted contact forms are actually delivered via email.

| Step | Action | Expected Result |
|---|---|---|
| 1 | Submit form with unique identifier in message | Form shows success |
| 2 | Check Formspree dashboard | Submission appears with all fields |
| 3 | Check destination email inbox | Email received within 5 minutes |
| 4 | Verify email contains all submitted fields | Name, company, email, inquiry type, message present |

## TC-003: Turnstile Rate Limiting Behavior

**Objective:** Verify behavior when Cloudflare rate-limits Turnstile challenges.

| Step | Action | Expected Result |
|---|---|---|
| 1 | Submit form 10+ times rapidly | Turnstile widget resets between submissions |
| 2 | If rate-limited, observe widget state | Widget should show a challenge or error, not hang |
| 3 | After rate limit expires, submit again | Form submits successfully |

## TC-004: Slow Network Conditions

**Objective:** Verify the site is usable on slow connections.

| Step | Action | Expected Result |
|---|---|---|
| 1 | Open DevTools > Network > Slow 3G | Page loads (may be slow) |
| 2 | Navigate using nav links | Smooth scroll still works |
| 3 | Submit contact form | "Sending..." state visible during wait, eventually succeeds or shows error |
| 4 | Verify no layout shifts during load | Content doesn't jump around as fonts/images load |
