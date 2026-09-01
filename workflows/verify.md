---
name: verify
description: Verify an implementation or existing change through scoped diff review, executable checks, runtime behavior, and an evidence-backed PASS or FAIL report.
version: 1.0.0
artifact_outputs: verification-scope, command-evidence, runtime-evidence, defect-list, pass-fail-report
---

# Generic verification

1. Identify the requested behavior and exact changed scope; do not broaden into unrelated auditing.
2. Review the diff and affected contracts for correctness, security, data, concurrency, errors, compatibility, and project conventions.
3. Run the narrowest relevant lint, type-check, build, unit/component/integration/E2E tests, and static validation.
4. Exercise the real entry point and applicable loading, empty, failure, retry, authorization, responsive, keyboard, or recovery states.
5. Use `verify-changes`; use `verify-and-stop` when the request is validation-only and fixes are not authorized.
6. Report PASS or FAIL with exact evidence. Separate verified facts, remaining defects, unverified areas, and environmental blockers.

