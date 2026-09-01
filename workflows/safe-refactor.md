---
name: safe-refactor
description: Restructure code while preserving externally observable behavior, contracts, data, and project conventions.
version: 1.0.0
requires_workflows: request-intake, verify
artifact_outputs: behavior-baseline, refactor-map, implementation, preservation-proof
---

# Generic safe refactor

1. Define the structural goal and explicit non-goals. Identify callers, contracts, generated files, extension points, tests, and ownership boundaries.
2. Capture a behavior baseline before edits using focused tests, build/type checks, runtime examples, snapshots, or contract fixtures.
3. Use `safe-refactor`; split the change into reviewable steps that keep the project runnable where practical.
4. Preserve public behavior, status semantics, serialization, ordering, persistence, authorization, localization, and compatibility unless explicitly changed.
5. Do not mix cleanup with new behavior. If a behavior change is required, route it as a separate feature or defect.
6. Re-run the baseline and inspect the diff for accidental semantic changes, dead compatibility paths, and incomplete caller migration.

