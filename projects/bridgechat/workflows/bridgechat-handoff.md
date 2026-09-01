---
name: bridgechat-handoff
description: Produce a concise BridgeChat handoff with contracts, distributed behavior, UI requirements, verification, and remaining work.
version: 3.0.0
requires_workflows: bridgechat-request-intake
artifact_outputs: handoff-report, frontend-contract, remaining-work
---

# /bridgechat-handoff

$ARGUMENTS

Report completed scope; impacted services/files; REST contracts; event/realtime contracts; DB/cache/broker changes; authorization; retries/idempotency/recovery; deploy order; frontend entry point/components/state/error/rollback behavior; localization files; and actual build/test/audit/runtime evidence. Separate completed, pending, deferred, and risky work. Do not expose secrets or claim unverified completion.
