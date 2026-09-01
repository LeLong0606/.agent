---
name: bridgechat-migrate
description: Migrate BridgeChat schemas, data, APIs, events, realtime contracts, configuration, or dependencies with mixed-version safety and deployment proof.
version: 1.0.0
requires_workflows: bridgechat-request-intake, bridgechat-brain-context, bridgechat-microservice-orchestration, bridgechat-text-integrity, bridgechat-verify, bridgechat-handoff, migration
artifact_outputs: ownership-map, compatibility-matrix, migration-plan, rollout-plan, recovery-plan, verification-report
---

# BridgeChat migration

1. Run intake and brain context; identify domain/data owner, Gateway, producers, consumers, frontend, storage, cache/search, broker, and shared-contract impact.
2. Use the generic `workflows/migration.md` and `migration` skill, then apply BridgeChat constraints.
3. Prefer additive schema and version-tolerant contracts. Deploy tolerant consumers before activating new producers; preserve old/new coexistence through the declared compatibility window.
4. Database execution belongs to the owning service Infrastructure layer using Dapper/raw SQL. Never use EF Core or write another service's database.
5. Version REST, integration-event, and realtime changes deliberately. Define correlation/causation/message IDs, ordering, deduplication, Outbox/Inbox behavior, Saga state, replay, reconciliation, and frontend convergence.
6. Backfills must be resumable, observable, bounded, idempotent, and safe under concurrent live traffic.
7. Test mixed versions, duplicate/out-of-order delivery, restart, timeout, partial backfill, stale cache/search, rollback or forward recovery, and Gateway/UI behavior.
8. Run text integrity, verification, and handoff with exact deploy/activation/removal order. Destructive cleanup requires explicit authorization and a later verified phase.

