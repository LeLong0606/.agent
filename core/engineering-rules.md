# Generic Engineering Rules

These rules apply to every project unless an active project profile explicitly
overrides them.

## Context First

- Identify the project, stack, affected layer, and ownership boundary before editing.
- Inspect existing conventions before introducing new architecture or dependencies.
- Preserve unrelated behavior and avoid opportunistic refactors unless requested.
- Prefer evidence from the repository over assumptions.

## Implementation

- Correctness before cleverness.
- Keep changes minimal, cohesive, and reversible.
- Reuse existing abstractions when they are appropriate; do not force reuse when it increases coupling.
- Keep boundaries explicit between UI, application/business logic, infrastructure, and external integrations.
- Never expose secrets, credentials, private keys, or privileged tokens in client code or committed configuration.

## Review Behavior

- Prefer fewer high-confidence findings over speculative breadth.
- Tie findings to exact files, routes, selectors, APIs, or code paths.
- Rank issues by impact: critical, high, medium, then low.
- Distinguish defects from optional improvements.
- When context is insufficient, state uncertainty instead of inventing a requirement.

## Verification

Before declaring a change complete:

1. Verify the requested behavior.
2. Run the narrowest relevant build, lint, test, type-check, or static analysis available.
3. Check regressions around changed boundaries.
4. Validate error/loading/empty states when applicable.
5. Report what was verified and what could not be verified.

## Project Isolation

- Never carry a project-specific rule into another project merely because it exists in `.agents`.
- Project conventions belong in `.agents/projects/<project>/`.
- Generic reusable knowledge belongs in `.agents/core/`, `.agents/skills/`, or `.agents/workflows/`.
