"""Accessibility helper — axe-core injection and scanning via Playwright."""

from axe_playwright_python.sync_playwright import Axe


def run_axe_scan(page, context=None, options=None):
    """Run an axe-core accessibility scan on the current page.

    Args:
        page: Playwright page object.
        context: Optional axe context (CSS selector or element reference).
        options: Optional axe run options (e.g., {"runOnly": ["wcag2aa"]}).

    Returns:
        AxeResults object with .violations, .passes, etc.
    """
    axe = Axe()
    results = axe.run(page)
    return results


def assert_no_violations(results, *, ignore_rules=None):
    """Assert that an axe scan found zero violations.

    Args:
        results: AxeResults from run_axe_scan.
        ignore_rules: Optional list of rule IDs to ignore (e.g., ["color-contrast"]).
    """
    violations = results.response.get("violations", [])

    if ignore_rules:
        violations = [v for v in violations if v["id"] not in ignore_rules]

    if violations:
        messages = []
        for v in violations:
            nodes = ", ".join(n["html"] for n in v.get("nodes", [])[:3])
            messages.append(
                f"  [{v['impact']}] {v['id']}: {v['description']} "
                f"({len(v['nodes'])} elements) — e.g. {nodes}"
            )
        raise AssertionError(
            f"Found {len(violations)} accessibility violation(s):\n"
            + "\n".join(messages)
        )
