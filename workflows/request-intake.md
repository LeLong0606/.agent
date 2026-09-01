---
name: request-intake
description: Normalize a natural-language engineering request, identify project scope and risk, and route it to the smallest applicable shared or project workflow.
version: 1.0.0
artifact_outputs: normalized-request, risk-flags, workflow-chain, selected-skills, definition-of-done
---

# Generic request intake

Use for engineering work when no project-specific intake workflow applies.

1. Extract intent, target, observable outcome, constraints, supplied evidence, exclusions, and authorization boundaries.
2. Identify the active project and load its profile when one exists. Project workflows override this generic router where intentionally stricter.
3. Classify relevant risk: security, data, contract, migration, UX, operations, destructive action, or text integrity.
4. Route to one primary workflow: `build-feature`, `build-ui`, `fix-error`, `safe-refactor`, `migration`, `verify`, or `media-production`.
5. Add `frontend-quality-gate` for frontend work and choose the smallest skill set from `core/skill-routing.md`.
6. Proceed with reasonable reversible assumptions. Ask only when ambiguity changes business behavior, public contracts, data ownership, security, destructive scope, or irreversible state.
7. Define completion through observable behavior and verification evidence rather than file creation alone.

