---
name: bridgechat-fix-error
description: Trace and fix BridgeChat defects across UI, Gateway, services, broker, storage, and realtime with regression proof.
version: 3.0.0
requires_workflows: bridgechat-request-intake, bridgechat-brain-context, bridgechat-skill-router, bridgechat-microservice-orchestration, bridgechat-text-integrity, bridgechat-verify
artifact_outputs: reproduction, root-cause, minimal-fix, regression-test, runtime-proof
---

# /bridgechat-fix-error — Evidence-first debugging

$ARGUMENTS

1. Run request intake to classify the symptom, supplied evidence, probable layers, risk, and debugging skills.
2. Run brain context and select debugging/domain skills.
3. Preserve Git state and capture timestamp, sanitized request, status/body, correlation ID, browser console, and container logs.
4. Reproduce and trace UI → Gateway → Controller → Handler → repository/broker/cache/DB → consumer/realtime → UI.
5. For cross-service defects, trace correlation/causation IDs, Outbox, Inbox/dedup, queues, retry/dead-letter, event version/order, Saga state, and reconciliation.
6. Before code, state symptom, root cause, evidence, why adjacent errors are secondary, and the regression test.
7. Apply the smallest source-of-truth fix. Never hide 409 with 200, add catch-all handling, retry forever, reset data, or delete volumes.
8. Frontend changes use bridgechatwebreact/public/locales/** only. Backend changes use Core.Localization resources only.
9. Re-run the original Gateway flow, verify side effects/logs, run regression and nearby happy paths, then run text-integrity and quality gates.
10. Report root cause, files/services, commands/tests, runtime proof, and risk. Do not commit/push/deploy unless requested.
