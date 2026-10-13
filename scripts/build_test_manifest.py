#!/usr/bin/env python3
"""Collect pytest tests and generate reproducible v6 test inventory documents."""
from __future__ import annotations
import json, re, subprocess, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
DOCS = ROOT / "docs"
DESCRIPTIONS = {
    "test_api.py": "API health/readiness, security headers, evidence and report bundles",
    "test_api_route_contract_matrix.py": "REST route, pagination, diff, cancel, report and evidence contracts",
    "test_checks.py": "Rule registry smoke test",
    "test_integration.py": "Local-only end-to-end demo scan and report generation",
    "test_scope.py": "Basic scope rules",
    "test_scope_matrix.py": "Legacy URL, host, port and exclusion matrix",
    "test_v4_security.py": "Origin credential isolation and transport guard regressions",
    "test_v5_api_extended.py": "API versioning, auth gate and assessment-plan contract",
    "test_v5_authz_matrix.py": "Read-only authorization comparison matrix",
    "test_v5_authz_policy.py": "Authorization policy and profile input matrix",
    "test_v5_browser_mock.py": "Browser discovery under mocked browser objects",
    "test_v5_cli.py": "CLI invocation, invalid target and report behavior",
    "test_v5_discovery_components.py": "Crawler, API discovery and bounded parameter-probe behavior",
    "test_v5_misc_invariants.py": "Cross-module safety invariants",
    "test_v5_redaction_matrix.py": "Original secret redaction regression matrix",
    "test_v5_risk_catalog.py": "Risk score and assessment catalog invariants",
    "test_v5_schema_matrix.py": "Input schema and malformed values",
    "test_v5_security_checks.py": "Cookie, header, CSP and API security checks",
    "test_v5_tls_matrix.py": "TLS parsing and connection error behavior",
    "test_v5_transport_report.py": "HTTP transport, redirect and report escaping",
    "test_v5_worker_planner_zap.py": "Worker queue, planner modes and ZAP plan safety",
    "test_security_regressions.py": "Credential encryption, secret redaction and earlier security fixes",
    "test_v6_scope_fuzz_matrix.py": "Adversarial URL, nested encoding, ports, scope joins and exclusion boundaries",
    "test_v6_redaction_fuzz_matrix.py": "Every registered sensitive field/query name plus recursive redaction matrix",
    "test_v6_risk_math_matrix.py": "Fine-grained severity/confidence risk scoring invariants",
    "test_v6_schema_hardening_matrix.py": "Boundary-value, header-injection and authorization profile schema checks",
    "test_v6_origin_credential_isolation.py": "Exact-origin credential guards including same-host different-port regression",
    "test_v6_catalog_report_contract.py": "Assessment/check catalog contracts and all report formats",
    "test_v6_http_method_and_redirect_matrix.py": "HTTP method, no-follow redirect and pre-network scope enforcement",
    "test_v6_rule_behavior_matrix.py": "Parameterized behavior checks for the registered passive and low-impact security rules",
    "test_v6_config_parser_matrix.py": "Environment configuration parser boundary and malformed-value handling",
}

def main() -> int:
    cmd = [sys.executable, "-m", "pytest", "--collect-only", "-q", "-o", "addopts=", "tests"]
    result = subprocess.run(cmd, cwd=BACKEND, capture_output=True, text=True)
    if result.returncode:
        print(result.stdout); print(result.stderr, file=sys.stderr)
        return result.returncode
    counts: Counter[str] = Counter()
    for line in (result.stdout + "\n" + result.stderr).splitlines():
        match = re.match(r"tests/(test_[^:]+\.py)::", line.strip())
        if match:
            counts[match.group(1)] += 1
    total = sum(counts.values())
    if total < 1:
        print("Could not parse pytest collection output", file=sys.stderr)
        return 2
    payload = {
        "release_version": "6.0.0",
        "test_count": total,
        "module_count": len(counts),
        "collection_command": "python -m pytest --collect-only -q -o addopts= tests (from backend/)",
        "modules": [{"file": name, "count": count, "focus": DESCRIPTIONS.get(name, "Unit and regression tests")}
                    for name, count in sorted(counts.items())],
        "interpretation": "Software regression tests and code coverage are not a percentage of vulnerabilities detected.",
    }
    (DOCS / "TEST_MANIFEST_V6.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# FIREWATCH v6 — Automated Test Matrix", "",
        "Release: `6.0.0`  ",
        f"Collected tests: **{total}** across **{len(counts)}** test modules.", "",
        "> This manifest is generated from pytest collection. Software test count and statement coverage are not the percentage of vulnerabilities found and do not prove that any target is secure.", "",
        "## Suite inventory", "",
        "| Test module | Collected cases | Focus |", "|---|---:|---|",
    ]
    for item in payload["modules"]:
        focus = item["focus"].replace("|", "\\|")
        lines.append(f"| `{item['file']}` | {item['count']} | {focus} |")
    lines += ["", f"| **Total** | **{total}** | All collected unit, matrix, regression, API and local demo tests |", "",
        "## Reproduce collection and run the suite", "", "```bash",
        "python -m pip install -r backend/requirements-dev.txt",
        "python scripts/build_test_manifest.py",
        "cd backend",
        "PYTHONPATH=. python -m pytest tests -q --cov=app --cov-report=term-missing --cov-fail-under=78",
        "```", "",
        "## Separate target assessment catalog", "",
        "The 79-item assessment plan is separate from software-regression tests. It labels checks requiring manual workflows, test accounts or specialist tools; those are not represented as automatically executed.",
        "See `ASSESSMENT_CATALOG.md`, `assessment-plan-v6.json`, and `assessment-plan-v6.csv`.", ""]
    (DOCS / "TEST_MATRIX_V6.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated docs/TEST_MANIFEST_V6.json and docs/TEST_MATRIX_V6.md: {total} tests in {len(counts)} modules.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
