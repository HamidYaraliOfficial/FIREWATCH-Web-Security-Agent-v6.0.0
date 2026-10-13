# FIREWATCH v6.0.0 Verification Record

Release target: `FIREWATCH-WebSec-Agent-v6.0.0`  
Verification date: `2026-10-12`  
Verification entry point: `python scripts/verify_release.py`

## Results

- **1,483 / 1,483 automated tests passed** across 31 test modules; zero failures, errors or skipped tests were recorded in the JUnit summary.
- **83.90% statement coverage** across `backend/app`, exceeding the enforced 78% threshold. This is code coverage, not the percentage of vulnerabilities found.
- Release gate result: **8 required checks passed, 0 failed**. Optional checks unavailable in the local environment are listed separately below.
- Python compilation passed for `backend/app`, `backend/tests` and `demo_target`.
- Dashboard JavaScript syntax check passed with Node.js.
- Publisher shell syntax check passed with Bash.
- Docker Compose YAML parsing passed. This validates YAML syntax only; it does not build an image or launch containers.
- Repository hygiene passed. The check is intentionally lightweight and is not a replacement for a full secret-scanning product.
- Assessment plan export succeeded and generated 79 entries: 22 automated passive checks, 13 automated review candidates, 38 manual/test-account cases and 6 specialist-tool cases.
- Test manifest generation succeeded: 1,483 collected test cases in 31 modules. See [`docs/TEST_MANIFEST_V6.json`](docs/TEST_MANIFEST_V6.json) and [`docs/TEST_MATRIX_V6.md`](docs/TEST_MATRIX_V6.md).

## Commands used

```bash
python scripts/verify_release.py

# The release script runs these core checks, among others:
python -m compileall -q backend/app backend/tests demo_target
node --check frontend/static/app.js
bash -n scripts/publish_to_github.sh
python scripts/repo_hygiene.py
python scripts/export_assessment_plan.py
python scripts/build_test_manifest.py
cd backend
PYTHONPATH=. python -m pytest tests -q --junitxml=<temporary-file> --cov=app --cov-report=term-missing --cov-fail-under=78
```

## Not executed / external verification required

- **Bandit:** skipped locally; executable not installed.
- **pip-audit:** skipped locally; executable not installed.
- **Docker Compose build/deployment:** skipped because Docker CLI/Engine is unavailable. Only Compose YAML parsing was checked.
- Re-installation of pinned dependencies from PyPI was not repeated; the installed build environment was used.
- Browser automation with a locally installed Chromium binary, actual ZAP scanning, GitHub-hosted CodeQL/CI, production PostgreSQL concurrency/load, and publishing to the user’s GitHub account are not claimed as locally completed.

## Assessment limitations

The separate 79-case assessment catalog intentionally differentiates automated passive checks, review candidates, manual/test-account workflows and specialist-tool checks. These are not all guaranteed to execute automatically in the built-in scanner. A passed regression suite is evidence about software behavior, not proof that the product detects all vulnerability classes. Scope checks should be combined with a dedicated outbound firewall/proxy allow-list because DNS validation alone is not a complete network isolation boundary. See [`docs/SECURITY_COVERAGE.md`](docs/SECURITY_COVERAGE.md) and [`SECURITY.md`](SECURITY.md).
