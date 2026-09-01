---
name: bridgechat-implement
description: Implement an approved BridgeChat plan in dependency-safe waves and preserve existing work.
version: 3.0.0
requires_workflows: bridgechat-request-intake, bridgechat-skill-router, bridgechat-microservice-orchestration, bridgechat-text-integrity
artifact_outputs: implementation, tests, verification-report
---

# /bridgechat-implement

$ARGUMENTS

Confirm the plan, inspect Git state, and preserve unrelated changes. Implement small vertical slices in dependency-safe order. Follow AGENTS.md for Dapper/Infrastructure, CQRS/VSA, validators, static routes, status codes, documentation, and localization. Keep frontend translations in bridgechatwebreact/public/locales/** and backend resources in Core.Localization. Build/test each wave, run distributed verification when needed, then run text-integrity until stable. Do not commit/push/deploy or expand scope without authorization.
