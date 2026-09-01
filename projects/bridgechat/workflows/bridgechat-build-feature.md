---
name: bridgechat-build-feature
description: Build a BridgeChat backend or full-stack feature end-to-end across all participating services.
version: 3.0.0
requires_workflows: bridgechat-request-intake, bridgechat-brain-context, bridgechat-skill-router, bridgechat-microservice-orchestration, bridgechat-text-integrity, bridgechat-verify, bridgechat-handoff
artifact_outputs: investigation, implementation-plan, implementation, tests, e2e-proof, handoff
---

# /bridgechat-build-feature — Feature delivery

$ARGUMENTS

1. Run bridgechat-request-intake to normalize the goal, scope, risks, definition of done, workflow chain, and skills.
2. Extract project and feature; resolve only unambiguous near-matches.
3. Run brain context and compare prior work with Git/source.
4. Select and read relevant skills.
5. Trace Controller/API through Application, Infrastructure, storage/broker/cache, consumers/realtime, Gateway, and frontend.
6. For multiple boundaries, run microservice orchestration and define impact graph, ownership, contracts, recovery, and deploy order before code.
7. Write a file-level plan for API, CQRS/validators, Dapper/SQL/migration, events, authorization, idempotency, concurrency, tests, and localization ownership. Continue unless plan approval or destructive authority is required.
8. Implement in dependency-safe waves and follow .agents/AGENTS.md.
9. Backend localization belongs only in BridgeChat.SharedLibraries/Core.Localization/Resources/{en-US,vi-VN,zh-CN}.json. Regenerate hover metadata.
10. Build/test every wave, then prove the Gateway/runtime flow and distributed failures.
11. Run text-integrity, architecture scans, localization audit, diff review, and final build until clean.
12. Report services, contracts, data/broker/cache/realtime changes, tests, deploy order, frontend handoff, and risks. Do not commit/push/deploy unless requested.
