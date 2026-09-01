---
name: build-ui
description: Build or change an application interface with real entry points, API integration, responsive states, accessibility, and browser proof.
version: 1.0.0
requires_workflows: request-intake, frontend-quality-gate, verify
artifact_outputs: ui-flow, component-tree, implementation, interaction-tests, browser-proof
---

# Generic UI delivery

1. Run `request-intake`; inspect the real route/entry point, design system, reusable components, state/data patterns, API contracts, and neighboring screens.
2. Define the UI flow and relevant loading, empty, populated, validation, submitting, success, failure, offline, timeout, retry, responsive, keyboard, and focus states.
3. Implement within the existing visual and architectural system. Keep UI, logic, data, validation, and types at their established boundaries.
4. For API-driven or realtime interfaces, model optimistic rollback, late responses, deduplication, reconnect, stale state, and server-truth reconciliation when applicable.
5. Run `frontend-quality-gate`, focused tests, type/lint/build checks, and browser verification through a reachable entry point.
6. A component that is unreachable, lacks applicable failure states, or cannot be exercised as visible UI is incomplete.

