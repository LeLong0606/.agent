---
name: build-feature
description: Build a backend or full-stack feature in an existing project from contract discovery through implementation and verification.
version: 1.0.0
requires_workflows: request-intake, verify
artifact_outputs: scope-map, implementation-plan, implementation, tests, verification-report
---

# Generic feature delivery

1. Run `request-intake`; inspect project instructions, architecture, neighboring features, contracts, tests, and reusable abstractions.
2. Map affected UI, API, application logic, data, integrations, events, operations, and ownership boundaries. Mark dependencies read-only until evidence requires edits.
3. Write a compact file-level plan when multiple boundaries or meaningful risk are involved.
4. Implement in dependency-safe waves. Preserve unrelated behavior and avoid opportunistic architecture changes.
5. Validate authorization, inputs, errors, concurrency, idempotency, compatibility, and recovery according to actual risk.
6. Add focused tests and verify through the real entry point when practical.
7. Run `verify` and any project-specific quality/text/deployment gates. Report completed, pending, unverified, and risky work separately.

