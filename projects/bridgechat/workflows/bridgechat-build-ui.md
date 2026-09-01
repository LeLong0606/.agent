---
name: bridgechat-build-ui
description: Design and implement a complete BridgeChat React interface, including visible components, interactions, responsive behavior, backend integration, and browser proof.
version: 3.1.0
requires_workflows: bridgechat-request-intake, bridgechat-brain-context, bridgechat-skill-router, bridgechat-microservice-orchestration, bridgechat-text-integrity, bridgechat-verify, bridgechat-handoff, frontend-quality-gate
artifact_outputs: ui-flow, component-implementation, api-integration, interaction-tests, browser-proof
---

# /bridgechat-build-ui — Actual UI delivery

$ARGUMENTS

Default project: bridgechatwebreact.

## Phase 0 — Context and contract

1. Run `bridgechat-request-intake` to identify the requested screen, entry point, backend dependencies, UX states, risks, and skills.
2. Run `bridgechat-brain-context` using bridgechatwebreact, the feature name, and related backend services.
3. Use `frontend-architecture` + `frontend-quality` as the normal frontend baseline. Add only the narrowly relevant supporting skills: `frontend-design` for visual-design work, `ui-styling` for actual Tailwind/shadcn/Radix detail, `nextjs-react-expert` for React/Next performance/framework issues, `i18n-localization` when text changes, and `webapp-testing` for browser/E2E proof.
4. Inspect the existing feature tree, design tokens, reusable primitives, routes, API clients, hooks, stores/cache, error handling, realtime subscriptions, and neighboring screens.
5. Read the real backend Controller/request/response/event contracts through Gateway. Never infer the contract from stale frontend code.
6. If multiple services/events participate, run the microservice orchestration workflow and map REST plus realtime convergence.

## Phase 1 — Specify the interface before coding

Produce a compact UI flow and component tree covering:

- The reachable entry point: button, menu, profile action, and visibility rules.
- Modal/page/panel composition and reused design-system components.
- Desktop and mobile layout.
- Loading, empty, populated, validation, submitting, success, partial-success, forbidden, conflict, offline, timeout, and retry states.
- Keyboard navigation, focus trap/return, accessible labels, screen-reader feedback, and disabled behavior.
- State transitions, cache updates, optimistic snapshot/rollback, and realtime deduplication.

This phase must describe an actual screen and interaction flow, not only API wiring.

## Phase 2 — Build the interface

1. Implement visible components and interactions within the existing design system. Do not create a parallel visual language.
2. Implement API types/adapters, hooks/mutations, state transitions, cache invalidation/merge, and navigation.
3. Every optimistic mutation requires a snapshot, rollback, late-response handling, and server-truth reconciliation.
4. Handle 400, 401, 403, 404, 409, 413, 415, 422, 429, 500, 502, 503, 504, and timeout according to the real endpoint contract.
5. Realtime handlers must be idempotent, unsubscribe correctly, survive reconnect, and avoid duplicate connections under React Strict Mode.
6. For Saga/eventual consistency, represent accepted, pending, completed, and failed states. Never treat 202 Accepted as business completion.

## Frontend localization boundary

All UI strings belong exclusively in `bridgechatwebreact/public/locales/**`, following the existing locale folders and namespaces. Use the frontend translation hook. Never add UI keys to Core.Localization and never use backend LocalizationKeys in React.

Backend API/log/validation localization remains exclusively in `BridgeChat.SharedLibraries/Core.Localization/Resources/*.json` and is outside this workflow unless backend code also changes.

## Phase 3 — Frontend quality gate and proof

1. Run the generic `.agents/workflows/frontend-quality-gate.md`. Its detailed source corpus is the cloned `/Google Drive/Front-End-Checklist` repository through `.agents/skills/frontend-quality/`.
2. Run typecheck, scoped lint, component/unit tests, and production build.
3. Use browser/E2E tooling when available. Exercise the complete click path at desktop and mobile widths.
4. Inspect the visible DOM result, focus behavior, browser console, network requests, status-specific messages, optimistic rollback, and realtime reconciliation.
5. A passing API call without a visible usable UI is FAIL.
6. A component that is not reachable from a real entry point is FAIL.
7. A screen without loading, empty, and error states is FAIL when those states can occur.
8. Run `bridgechat-text-integrity` on changed frontend files and `bridgechatwebreact/public/locales/**`. Do not scan or modify backend localization unless backend code changed.

Report browser observations/screenshots, component files, entry point, API/event contracts, state/error behavior, tests/build/audit, and backend gaps. Do not commit or push unless requested.
