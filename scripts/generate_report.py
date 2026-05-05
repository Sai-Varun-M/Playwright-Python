"""
generate_report.py
Merges all Playwright JSON result files in playwright-report/
and writes dashboard/data.js so the HTML dashboard can read them.

Usage:
    python scripts/generate_report.py
"""
from __future__ import annotations

import json
import os
import glob
from datetime import datetime
from pathlib import Path


REPORT_DIR    = Path("playwright-report")
DASHBOARD_DIR = Path("dashboard")
OUTPUT_JS     = DASHBOARD_DIR / "data.js"


def load_json_reports() -> list[dict]:
    """Find and load all *-results.json files."""
    patterns = [
        str(REPORT_DIR / "results.json"),
        str(REPORT_DIR / "*-results.json"),
    ]
    files: list[str] = []
    for pattern in patterns:
        files.extend(glob.glob(pattern))

    reports = []
    for fpath in sorted(set(files)):
        try:
            with open(fpath) as f:
                reports.append(json.load(f))
            print(f"  ✓ Loaded: {fpath}")
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"  ✗ Skipped {fpath}: {e}")
    return reports


def extract_tests(report: dict) -> list[dict]:
    """Flatten a pytest-json-report JSON into a list of test records."""
    tests = []
    for test in report.get("tests", []):
        outcome = test.get("outcome", "unknown")
        duration = test.get("call", {}).get("duration", 0) if "call" in test else 0
        node_id  = test.get("nodeid", "")

        # Parse suite from node_id: tests/smoke/test_smoke.py::TestSmoke::test_foo
        parts = node_id.split("/")
        suite = parts[1] if len(parts) > 1 else "unknown"

        # Parse browser from keywords if present (pytest-json-report returns a list)
        raw_keywords = test.get("keywords", [])
        if isinstance(raw_keywords, dict):
            keywords = list(raw_keywords.keys())
        else:
            keywords = list(raw_keywords)
        browser = next((k for k in keywords if k in ("chromium", "firefox", "webkit")), "chromium")

        tests.append({
            "id":       node_id,
            "name":     node_id.split("::")[-1],
            "suite":    suite,
            "browser":  browser,
            "status":   outcome,           # passed / failed / skipped
            "duration": round(duration * 1000),  # convert to ms
            "error":    (test.get("call", {}) or {}).get("longrepr", ""),
        })
    return tests


def build_summary(all_tests: list[dict]) -> dict:
    statuses = [t["status"] for t in all_tests]
    total    = len(statuses)
    passed   = statuses.count("passed")
    failed   = statuses.count("failed")
    skipped  = statuses.count("skipped")
    durations = [t["duration"] for t in all_tests]

    return {
        "total":    total,
        "passed":   passed,
        "failed":   failed,
        "skipped":  skipped,
        "passRate": round(passed / total * 100, 1) if total else 0,
        "totalDurationMs": sum(durations),
        "avgDurationMs":   round(sum(durations) / total) if total else 0,
        "generatedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def build_suite_breakdown(all_tests: list[dict]) -> list[dict]:
    suites: dict[str, dict] = {}
    for t in all_tests:
        s = t["suite"]
        if s not in suites:
            suites[s] = {"suite": s, "passed": 0, "failed": 0, "skipped": 0, "total": 0}
        suites[s][t["status"]] += 1
        suites[s]["total"] += 1
    return list(suites.values())


def build_browser_breakdown(all_tests: list[dict]) -> list[dict]:
    browsers: dict[str, dict] = {}
    for t in all_tests:
        b = t["browser"]
        if b not in browsers:
            browsers[b] = {"browser": b, "passed": 0, "failed": 0, "total": 0}
        if t["status"] in ("passed", "failed"):
            browsers[b][t["status"]] += 1
        browsers[b]["total"] += 1
    return list(browsers.values())


def write_dashboard_data(summary: dict, tests: list[dict],
                         suites: list[dict], browsers: list[dict]) -> None:
    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "summary":          summary,
        "tests":            tests,
        "suiteBreakdown":   suites,
        "browserBreakdown": browsers,
    }
    js_content = f"window.REPORT_DATA = {json.dumps(payload, indent=2)};\n"
    OUTPUT_JS.write_text(js_content)
    print(f"\n✅ Dashboard data written to {OUTPUT_JS}")
    print(f"   Total: {summary['total']}  Passed: {summary['passed']}  "
          f"Failed: {summary['failed']}  Skipped: {summary['skipped']}  "
          f"Pass rate: {summary['passRate']}%")


def main() -> None:
    print("\n🔍 Scanning for JSON reports …")
    reports = load_json_reports()

    if not reports:
        print("⚠️  No JSON reports found. Generating empty dashboard.")
        # Write empty data so dashboard still renders
        write_dashboard_data(
            {"total": 0, "passed": 0, "failed": 0, "skipped": 0,
             "passRate": 0, "totalDurationMs": 0, "avgDurationMs": 0,
             "generatedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
            [], [], []
        )
        return

    all_tests: list[dict] = []
    for report in reports:
        all_tests.extend(extract_tests(report))

    summary  = build_summary(all_tests)
    suites   = build_suite_breakdown(all_tests)
    browsers = build_browser_breakdown(all_tests)

    write_dashboard_data(summary, all_tests, suites, browsers)


if __name__ == "__main__":
    main()
