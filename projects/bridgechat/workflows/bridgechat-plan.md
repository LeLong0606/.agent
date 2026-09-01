---
name: bridgechat-plan
description: Produce a reviewable BridgeChat implementation plan for a feature or defect.
version: 3.0.0
requires_workflows: bridgechat-request-intake, bridgechat-brain-context, bridgechat-skill-router, bridgechat-microservice-orchestration
artifact_outputs: implementation-plan, contracts, verification-plan
---

# /bridgechat-plan

$ARGUMENTS

Read current code and reuse existing abstractions. Define impacted services/layers, ownership, endpoints, CQRS slices, validators, repositories/SQL, migrations, events/consumers, realtime, frontend state, localization ownership, authorization, transactions, idempotency, concurrency, failure recovery, deploy order, test matrix, and completion criteria. Frontend translations use bridgechatwebreact/public/locales/**; backend resources use Core.Localization only. This workflow plans only and waits for approval when the user requested a plan gate.
