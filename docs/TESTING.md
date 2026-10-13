# Testing Guide — FIREWATCH v6.0.0

## Automated regression suite

The v6 suite contains **1,483 collected pytest cases across 31 test modules**. In the local release-gate run, all 1,483 passed, with zero failures, errors or skips. `pytest-cov` reported **83.90% statement coverage**. CI enforces a 78% minimum. Test count and statement coverage are not percentages of vulnerabilities detected and do not prove that a target is secure.

Install the development dependencies and run the same coverage gate used for release validation:

```bash
python -m pip install -r backend/requirements-dev.txt
python scripts/build_test_manifest.py
cd backend
PYTHONPATH=. python -m pytest tests -q -rA --cov=app --cov-report=term-missing --cov-report=xml:../coverage.xml --cov-fail-under=78
```

To run all local release checks (compilation, JavaScript and shell syntax, YAML parsing, repository hygiene, regenerated catalogs, the test suite and coverage gate):

```bash
python scripts/verify_release.py
```

Optional Bandit, pip-audit and Docker checks run only when the corresponding executable is available; the verification script clearly prints when an optional tool was skipped.

## Test inventory

The generated inventory in [`TEST_MATRIX_V6.md`](TEST_MATRIX_V6.md) lists the collected case count and focus of each of the 31 modules. `TEST_MANIFEST_V6.json` is intended for tools and CI. Its suites cover API route contracts, worker and local demo integration, URL/host/port policies, multi-layer URL encoding, credential origin isolation, sensitive-data redaction, schema boundaries, risk scoring, finding/report consistency, low-impact rule behavior and configuration parsing.

## Separate assessment-plan export

The **79-case assessment catalog** is separate from software regression tests. It includes 22 automated passive checks, 13 automated review candidates, 38 manual/test-account cases and 6 specialist-tool cases. Regenerate JSON, CSV and Markdown after catalog changes:

```bash
python scripts/export_assessment_plan.py
```

The API serves the plan at `GET /api/v1/assessment-plan`. Manual or specialist-tool entries are not represented as automatically run by the built-in safe scanner.

## Static checks and CI

CI tests Python 3.11, 3.12 and 3.13, enforces at least 78% coverage, validates the regenerated catalogs/manifests, checks dashboard JavaScript and publisher shell syntax, parses Docker Compose YAML, runs repository hygiene, and configures Bandit and pip-audit. CodeQL runs in its own workflow. Hosted results should only be treated as verified after the real GitHub Actions runs complete.

## Manual browser / deployment validation

Playwright's Chromium binary is required for real browser discovery. Confirm browser requests stay in scope, forms are not submitted, downloads are not accepted, configured credentials are never sent to other origins/ports or public HTTP, and secrets do not leak into evidence. Docker image building, PostgreSQL production deployment, external worker processing, ZAP reachability/scan jobs and hosted CI remain separate verification activities.

## Demo result interpretation

The included demo target is intentionally weak to exercise known detector paths. Expected findings can change as rules evolve. Tests should assert the rule behavior, safe transport, evidence sanitization, and pipeline completion rather than assume a finding count proves complete security coverage.
