---
name: fix-error
description: Diagnose and fix a defect from reproducible evidence and root cause through a narrow regression-proven change.
version: 1.0.0
requires_workflows: request-intake, verify
artifact_outputs: reproduction, root-cause, fix, regression-test, verification-report
---

# Generic defect fix

1. Capture the exact symptom, expected result, reproduction, environment, logs/status/body/stack trace, and recent relevant changes.
2. Use the fast path for a clear failure point; use `systemic-debugging` for intermittent, cross-layer, timing, state-lifecycle, or silent failures.
3. Prove the root cause before editing. Distinguish primary cause from downstream symptoms.
4. Apply `surgical-patch` at the narrowest responsible source-of-truth boundary after the cause is established.
5. Add a regression test or equivalent executable proof, rerun the original reproduction, and check adjacent success/failure paths.
6. Do not hide semantic errors with generic success, catch-all handling, infinite retry, data reset, or unrelated refactoring.

