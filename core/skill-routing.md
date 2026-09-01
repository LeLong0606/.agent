# Shared Skill Routing

Use the smallest effective skill set. Skills are project-neutral by default; project profiles specialize how they are applied.

Consult `.agents/core/skill-catalog.md` when two or more skills overlap or when a vendor-specific skill is being considered.

## Primary routing by concern

- Architecture/system boundaries: `architecture`; add `api-patterns` or `database-design` only when API/data design is materially involved.
- .NET/CQRS/VSA: `dotnet-clean-arch-vsa`; add `api-patterns` for HTTP contracts and `database-design` for schema/query/transaction design.
- Frontend structure: `frontend-architecture`.
- Frontend visual design: `frontend-design`; add `ui-styling` only when the project actually uses shadcn/ui, Tailwind, Radix, or closely related implementation patterns.
- Frontend quality/review: `frontend-quality` is the default project-neutral quality gate and includes a bundled portable checklist.
- React/Next.js performance: `nextjs-react-expert` only when React/Next framework behavior or performance is materially involved.
- Security: prefer defensive review skills (`backend-security-defense`, `frontend-security-defense`, `vulnerability-scanner`). Use `red-team-tactics` only for an explicitly appropriate adversarial/security-assessment task.
- Debugging: prefer `systemic-debugging`; it contains both a fast path for clear failures and a wider cross-layer root-cause path. Use `investigate` for focused evidence gathering.
- Tests: `testing-patterns` for strategy, `tdd-workflow` for test-first implementation, `webapp-testing` for browser/E2E.
- Code review: `code-review-checklist` for portable generic review; use the vendor `review` skill only when its gstack pre-landing workflow is explicitly desired and supported.
- Quality/verification: `verify-changes` is the default proof-of-work skill; add `lint-and-validate` when lint/type/schema validation applies. `checking-minor-errors` is an optional lightweight final pass, not a mandatory companion to every task.
- Localization: `i18n-localization`; project profile defines resource ownership.
- Multi-domain coordination: `coordinator-mode` or `parallel-agents` only when work can be safely partitioned.
- Deployment/operations: `deployment-procedures`, `server-management`, `bash-linux`, or `powershell-windows` based on environment.
- Brand/logo/banner/social/slides design: `design`; do not use it as the default skill for application UI.
- Browser CLI work: choose only the matching `agent-browser-*` skill and only when its runtime is available; ordinary browser/E2E proof still defaults to `webapp-testing`.
- UI motion: use `animate` for general motion decisions or one matching `gsap-*` skill for GSAP-specific implementation; do not load the whole animation suite.
- Product/marketing: select one narrow marketing skill for the requested outcome; do not load the imported marketing collection as a bundle.
- Narrow implementation change: add `surgical-patch` for a small defect/behavior edit, `safe-refactor` for behavior-preserving restructuring, or `migration` for compatibility-safe transitions.
- Video/motion composition: start with `hyperframes`, then load only the routed companion matching the requested artifact.

## Overlap policy

Avoid stacking multiple broad skills that solve the same problem.

- `systematic-debugging` is a compatibility alias for `systemic-debugging`; do not load both.
- `investigate-first` overlaps the default debugging path; prefer `systemic-debugging` + `investigate` unless its evidence-ranked compact workflow is specifically requested.
- `verify-and-stop` overlaps `verify-changes`; use it only when validation must explicitly forbid any scope expansion.
- `frontend-quality` is the common frontend quality gate. Do not load hundreds of Front-End-Checklist micro-skills into normal context.
- `web-design-guidelines` is opt-in for the Vercel Web Interface Guidelines specifically; it does not replace the default Front-End-Checklist-based quality gate.
- Do not load `qa`, `qa-only`, `review`, `code-review-checklist`, and `verify-changes` together by default. Choose the narrowest combination required.
- `qa`, `qa-only`, and `review` are vendor/gstack orchestration skills with substantial runtime assumptions. Prefer portable skills unless that environment/workflow is intentionally being used.
- For application UI, prefer `frontend-design` + `frontend-architecture` as needed. Add `ui-styling` only for its concrete stack. Keep `design-review`, `design-shotgun`, and `design-consultation` specialized/opt-in.
- Do not load `frontend-design`, `ui-styling`, `design`, `design-review`, `design-shotgun`, and `design-consultation` as one bundle.

## Front-End Checklist source policy

The portable detailed corpus is bundled at `skills/frontend-quality/references/portable-checklist.md`.

- Default: load `skills/frontend-quality/SKILL.md`.
- Deep audit or uncertain rule: consult `skills/frontend-quality/references/front-end-checklist.md`, then load only the relevant category from the bundled portable checklist.
- Front-End Checklist MCP tools may supplement the bundled corpus when available, but portable execution must not depend on them.

## Project isolation

A project profile may require or forbid techniques, but it must not redefine a shared skill as globally mandatory. Shared skills remain reusable across projects.

## New skill and corpus intake

When the user supplies another skill repository or corpus:

1. Inspect its entry skill, references, scripts, workflows, runtime assumptions, and overlap with the current catalog.
2. Extract reusable decisions into the smallest appropriate shared skill, reference, script, or generic workflow.
3. Keep vendor tooling optional unless it is required by the user's active environment.
4. Put BridgeChat-only contracts, service ownership, localization paths, Gateway/realtime behavior, and verification rules under `projects/bridgechat/`.
5. Update BridgeChat workflows to compose the shared capability when it improves BridgeChat delivery.
6. Verify the shared capability can still be selected and used for a non-BridgeChat project without loading BridgeChat instructions.

Do not copy an entire external catalog into normal runtime context. Preserve useful depth through focused references and load them only when the task requires them.
