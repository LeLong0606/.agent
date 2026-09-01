---
name: bridgechat-ui-polish
description: Audit and polish an existing BridgeChat interface without inventing new product behavior, while preserving realtime, localization, responsive, and accessibility behavior.
version: 1.0.0
requires_workflows: bridgechat-request-intake, bridgechat-brain-context, bridgechat-text-integrity, bridgechat-verify, frontend-quality-gate
artifact_outputs: visual-audit, polish-scope, implementation, before-after-proof
---

# BridgeChat UI polish

1. Run intake and brain context; identify the real route, entry point, current screenshots/rendered state, design tokens, reusable primitives, and relevant API/realtime states.
2. Use `frontend-quality` plus `impeccable`. Add `frontend-design`, `ui-styling`, `animate`, or one matching `gsap-*` skill only for a distinct requested concern.
3. Rank supported issues by user impact: unreachable/confusing interaction, hierarchy, density, responsive failure, accessibility, state feedback, typography, spacing, color, motion, then cosmetic consistency.
4. Preserve business behavior, contracts, optimistic rollback, realtime reconciliation, error/status handling, locale ownership, and existing design language unless the request explicitly changes them.
5. Exercise loading, empty, populated, error, offline, pending, rollback, reconnect, long translations, keyboard/focus, desktop, and mobile states that apply.
6. Produce before/after browser evidence from a real entry point. A static component mock without the reachable flow and state proof is incomplete.

