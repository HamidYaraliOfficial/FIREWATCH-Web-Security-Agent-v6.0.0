# FIREWATCH Web Security Agent v6.0.0

FIREWATCH v6 is a security-assessment and test-quality release. It expands the automated regression suite to 1,483 collected tests and tightens URL/credential handling based on issues found during test development.

## Release highlights

- **1,483 automated regression tests across 31 test modules**, including parameterized matrices, REST API routes, rule behavior, redaction, schema boundaries, credential isolation, reports, worker/planner behavior and the local end-to-end demo scan.
- **83.90% Python statement coverage** in the local release-gate environment; CI enforces a 78% minimum. Coverage is not a percentage of vulnerabilities detected.
- **79-item assessment plan**, served by `/api/v1/assessment-plan` and included as JSON, CSV and Markdown. The entries distinguish automated passive checks, automated review candidates, manual/test-account cases and specialist-tool cases.
- Credential material is limited to the exact root origin (scheme, host and effective port), and public targets require HTTPS for configured credentials. Browser request interception follows the same policy.
- Nested URL query values are recursively redacted with a depth cap; exclusion comparisons normalize repeated URL decoding without rewriting the actual request URL. HTTP `TE` and `Trailer` headers are blocked in user-supplied request/profile headers.
- Regression coverage includes HTTP redirect behavior, scope exclusions, nested secrets, API authentication gates, route contracts, HTML/CSV/SARIF behavior, risk math, configuration parsing, catalog/report consistency and mock-only transport isolation.
- CI matrix covers Python 3.11, 3.12 and 3.13 with a 78% coverage gate, JavaScript syntax, generated-document consistency, repository hygiene, Docker Compose YAML parsing, Bandit high-severity/high-confidence checks and dependency audit.

## Validation performed locally for this package

- Release gate: **8 required checks passed, 0 failed**.
- Pytest: **1,483 passed, 0 failed, 0 errors, 0 skipped** (JUnit output collected by `scripts/verify_release.py`).
- `pytest-cov`: **83.90% total statement coverage**, meeting the required 78% minimum.
- Python compile, dashboard JavaScript syntax, publisher shell syntax, Docker Compose YAML parsing, repository hygiene, assessment-plan export and test-manifest generation passed.
- The generated test manifest records 1,483 collected tests across 31 modules. The separate assessment plan contains 79 control entries.

## Checks not run or not claimed locally

- Bandit and pip-audit executables were unavailable in this build environment; these tools are configured in CI but are **not** counted as locally passed.
- Docker CLI/Engine was unavailable; Compose YAML parsed successfully, but no Docker image/container build is claimed.
- Chromium-backed browser automation, active/passive ZAP execution, GitHub-hosted CodeQL, production PostgreSQL concurrency/load and public GitHub publishing were not claimed as completed here.
- Outbound dependency installation was not repeated as part of this release gate; the installed local environment was used.

## Safety and interpretation

FIREWATCH is for systems where the operator has explicit authorization. The default assessment path is bounded and non-destructive. It does not execute brute-force or credential-stuffing campaigns, destructive business operations, arbitrary SQL/shell injection payloads or weaponized SSRF chains. Some authorization, business-logic, injection and authentication findings require dedicated test identities, application-specific fixtures and human validation. Passing the software test suite does not prove that the scanner finds every vulnerability or that an assessed site is secure.
