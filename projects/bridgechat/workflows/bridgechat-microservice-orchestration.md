---
name: bridgechat-microservice-orchestration
description: Coordinate BridgeChat features across services, data owners, contracts, events, realtime, recovery, and rollout.
version: 3.0.0
requires_workflows: bridgechat-request-intake, bridgechat-brain-context, bridgechat-skill-router, bridgechat-text-integrity
artifact_outputs: service-impact-graph, contract-map, consistency-plan, rollout-plan, e2e-proof
---

# /bridgechat-microservice-orchestration — Distributed delivery

$ARGUMENTS

Use when two or more services, Gateway, shared contracts, broker events, realtime, or frontend participate.

1. Build a service-impact graph. Mark each service IN, READ-ONLY DEPENDENCY, or OUT and assign domain/data owner, API entry, Saga coordinator, producer, consumer, realtime, notification, search, blob, identity, or frontend responsibility. Never write another service's database.
2. Choose sync calls, choreography, or a persisted orchestrated Saga deliberately. Never simulate a distributed transaction. Keep local state plus Outbox atomic and use Inbox/dedup for consumers.
3. Define REST, integration-event, and realtime contracts before code, including version, correlation/causation/message IDs, status mapping, authorization, ordering, and deduplication.
4. Design idempotency, concurrency, retry/backoff, timeout, circuit breaker, dead-letter, compensation/reconciliation, PII boundaries, and deletion propagation.
5. Implement in deployable waves: additive contract/schema; tolerant consumers; domain owner/API/Outbox; downstream consumers/read models; Gateway/realtime; frontend; producer activation.
6. Test duplicate and out-of-order delivery, timeout, broker outage, Outbox replay, dead-letter, restart during Saga, authorization, stale cache/search, and realtime reconnect.
7. Verify through Gateway with real containers when practical and correlate logs, owner databases, queues, cache/search, and UI.
8. Report Service | Role | Contract/files | Data/broker change | Test | Deploy order, plus recovery and risk.
