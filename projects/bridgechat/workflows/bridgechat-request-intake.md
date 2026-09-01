---
name: bridgechat-request-intake
description: Analyze any natural-language BridgeChat request, infer scope and risks, then automatically select the correct workflow chain and skills before work begins.
version: 3.1.0
artifact_outputs: normalized-request, scope-map, risk-classification, workflow-chain, selected-skills, clarification-gate
---

# /bridgechat-request-intake — Requirement analysis and automatic routing

$ARGUMENTS

Run this before brain lookup, investigation, planning, implementation, UI work, or debugging. The user does not need to name workflows or skills.

## 1. Normalize the request

Extract and restate:

- **Intent:** investigate, plan, build backend, build UI, fix defect, verify, hand off, commit/push, deploy, or destructive operation.
- **Target:** repository, microservice, shared library, frontend feature, endpoint, event, database, queue, or screen.
- **Desired outcome:** the observable behavior that must exist when work is complete.
- **Inputs and constraints:** examples, status codes, limits, security rules, localization, compatibility, deadlines, explicit exclusions, and approval gates.
- **Evidence supplied:** logs, stack trace, screenshot, browser console, container ID, file path, PID, walkthrough path, or reproduction steps.

Do not silently replace the user's business language with an implementation assumption. Preserve exact limits and distinctions such as global deletion versus hide-for-self, direct chat versus group, or accepted versus completed.

## 2. Discover implied scope

Infer likely participants without assuming they all require edits:

| Signal | Candidate scope |
|---|---|
| Message, conversation, receipt, reaction | MessageService, ConnectionService, frontend chat |
| Attachment, image, video, file | AttachmentService, MessageService, storage, frontend attachment/chat |
| Group membership or dissolution | GroupService, MessageService, AttachmentService, NotificationService, realtime, frontend |
| Login, OTP, key, session, permission | IdentityService, NotificationService, Gateway, frontend auth/E2EE |
| Presence or typing | PresenceService, ConnectionService, frontend realtime |
| Search/index | SearchService, owner service events, frontend search |
| Route/status mismatch | Frontend, API Gateway, destination controller |
| Eventual consistency or partial failure | Producer, broker contract, consumers, Outbox/Inbox/Saga/reconciler |

Mark each candidate as `PROBABLE`, `DEPENDENCY TO VERIFY`, or `OUT`. Investigation must confirm the final impact graph before edits.

## 3. Classify risk and required depth

Assign one or more flags:

- `SECURITY`: authentication, authorization, membership, PII, upload, encryption.
- `DISTRIBUTED`: multiple services, events, Saga, eventual consistency.
- `DATA`: schema, migration, deletion, concurrency, retention.
- `CONTRACT`: REST/event/realtime/shared type changes.
- `UX`: visible interaction, optimistic state, accessibility, responsive behavior.
- `OPERATIONS`: Docker, queue, deployment, replay, cleanup job.
- `TEXT_INTEGRITY`: localization, generated metadata, UTF-8/CRLF, mojibake.

Risk determines verification depth. High-risk work requires negative tests and runtime proof; a successful compile alone is insufficient.

## 4. Resolve ambiguity without unnecessary pauses

Proceed with a stated assumption when it is reversible, local, and consistent with existing code. Ask the user before acting only when ambiguity changes business behavior, public contract, data ownership, destructive scope, production state, security posture, or an irreversible operation.

If the user explicitly requests investigation/plan before code, enforce that gate. Otherwise continue through the selected workflow chain automatically.

## 5. Select the workflow chain

Choose one primary chain from `.agents/projects/bridgechat/workflows/`:

- Backend or full-stack feature: `bridgechat-build-feature.md`.
- Visible React feature: `bridgechat-build-ui.md`; include backend contract inspection.
- Defect, 4xx/5xx, incorrect data, logs, or regression: `bridgechat-fix-error.md`.
- Report-only investigation: `bridgechat-investigate.md`.
- Plan-only request: `bridgechat-plan.md`.
- Verification/review only: `bridgechat-verify.md`.
- Handoff only: `bridgechat-handoff.md`.

Always prepend `bridgechat-brain-context.md`. Add `bridgechat-microservice-orchestration.md` for `DISTRIBUTED` or cross-boundary `CONTRACT` work. Always append `bridgechat-text-integrity.md` and verification before completion.

For frontend/UI work, also append the generic `.agents/workflows/frontend-quality-gate.md`.

## 6. Select skills automatically

Read `bridgechat-skill-router.md` plus `.agents/core/skill-routing.md`, then select only skills that create a concrete decision or verification step.

Typical mapping:

- Architecture/boundaries: `architecture`; add `api-patterns` or `database-design` only when needed.
- .NET backend: `dotnet-clean-arch-vsa`; add `clean-code` when source changes materially benefit from it.
- React UI structure: `frontend-architecture`.
- Visible UI quality/accessibility: `frontend-quality`; add `frontend-design` for visual-design work.
- Tailwind/shadcn/Radix detail: `ui-styling` only when that stack is actually present.
- React/Next performance: `nextjs-react-expert` only for framework/performance depth.
- Security: defensive security skills by default; adversarial/red-team only when explicitly appropriate.
- Debugging: `systemic-debugging`; add `investigate` for focused evidence gathering.
- Tests: `testing-patterns`, `tdd-workflow`, or `webapp-testing` according to the actual verification need.
- Quality proof: `verify-changes`; add `lint-and-validate` where applicable.
- Localization: `i18n-localization`, respecting frontend/backend ownership.
- Parallel multi-domain work: `coordinator-mode` or `parallel-agents` only when safe partitioning actually helps.

Do not load compatibility duplicates or vendor/gstack orchestration skills merely because their trigger text loosely matches. Consult `.agents/core/skill-catalog.md` for status.

Announce the selected workflow chain and skills in one concise update, including why each group is relevant. Then read every selected `SKILL.md` completely before acting.

## 7. Produce the execution brief

Before tool-heavy work, produce an internal brief:

```text
Normalized goal:
Primary workflow:
Additional workflows:
Probable scope:
Explicitly out of scope:
Risk flags:
Selected skills and reasons:
Assumptions:
Clarification/approval required:
Definition of done:
```

Keep the user-facing version to 2–5 lines unless they request the full plan. The brief is a routing artifact, not a reason to delay execution.

## 8. Completion guard

Before reporting completion, compare results against the normalized goal and definition of done. Do not substitute adjacent work for the requested outcome. Report `BLOCKED` with evidence when a required contract, permission, environment, or business decision is unavailable.
