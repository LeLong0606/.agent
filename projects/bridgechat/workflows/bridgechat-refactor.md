---
name: bridgechat-refactor
description: Refactor BridgeChat code while preserving REST, event, realtime, data, localization, and runtime behavior across affected services.
version: 1.0.0
requires_workflows: bridgechat-request-intake, bridgechat-brain-context, bridgechat-text-integrity, bridgechat-verify, bridgechat-handoff, safe-refactor
artifact_outputs: behavior-baseline, boundary-map, refactor, preservation-proof
---

# BridgeChat safe refactor

1. Run intake and brain context; state the structural goal and explicitly exclude feature or contract changes.
2. Use the generic `workflows/safe-refactor.md` and `safe-refactor` skill.
3. Map Controller/Gateway routes, Commands/Queries/Validators, Application/Infrastructure boundaries, Dapper repositories, events/realtime contracts, frontend callers, localization ownership, and generated files.
4. Capture focused behavior and contract baselines before editing. For cross-service code, add microservice orchestration without changing service/data ownership.
5. Preserve explicit lowercase routes, semantic status codes, request/response serialization, event versions, ordering/idempotency, realtime convergence, Dapper ownership, and localization placement.
6. Never hand-edit generated localization code or move frontend text into backend resources.
7. Refactor in dependency-safe waves and rerun the baseline, builds/tests, runtime/Gateway path, text integrity, and diff review after each meaningful boundary move.

