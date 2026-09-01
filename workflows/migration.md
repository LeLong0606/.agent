---
name: migration
description: Plan and implement a compatibility-safe transition across schema, data, API, protocol, configuration, or dependencies.
version: 1.0.0
requires_workflows: request-intake, verify
artifact_outputs: current-target-map, compatibility-plan, rollout-plan, migration, rollback-or-forward-recovery, verification-report
---

# Generic migration

1. Define current state, target state, owners, consumers, invariants, compatibility window, data volume, and irreversible steps.
2. Prefer expand/migrate/contract: add tolerant structures/contracts, deploy compatible producers and consumers, migrate/backfill with checkpoints, verify, then remove legacy paths later.
3. Use the `migration` skill and applicable data/API/deployment skills. Separate schema, data, code, config, and traffic activation steps.
4. Specify idempotency, resumption, batching, locking/concurrency, partial failure, observability, backup, rollback or forward recovery, and deploy order.
5. Test mixed-version operation, retry/restart, old/new readers and writers, malformed legacy data, and interruption at each meaningful phase.
6. Never perform destructive production migration, legacy removal, or irreversible activation without explicit authority.

