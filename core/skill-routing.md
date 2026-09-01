# Shared Skill Routing

Use the smallest effective skill set. Skills are project-neutral by default; project profiles specialize how they are applied.

Consult `.agents/core/skill-catalog.md` when two or more skills overlap or when a vendor-specific skill is being considered.

## Primary routing by concern

- Architecture/system boundaries: `architecture`; add `api-patterns` or `database-design` only when API/data design is materially involved.
- .NET/CQRS/VSA: `dotnet-clean-arch-vsa`; add `api-patterns` for HTTP contracts and `database-design` for schema/query/transaction design.
- Frontend structure: `frontend-architecture`.
- Frontend visual design: `frontend-design`; add `ui-styling` only when the project actually uses shadcn/ui, Tailwind, Radix, or closely related implementation patterns.
- Frontend quality/review: `frontend-quality` is the default project-neutral quality gate and is distilled from the cloned Front-End-Checklist corpus.
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

## Overlap policy

Avoid stacking multiple broad skills that solve the same problem.

- `systematic-debugging` is a compatibility alias for `systemic-debugging`; do not load both.
- `frontend-quality` is the common frontend quality gate. Do not load hundreds of Front-End-Checklist micro-skills into normal context.
- `web-design-guidelines` is opt-in for the Vercel Web Interface Guidelines specifically; it does not replace the default Front-End-Checklist-based quality gate.
- Do not load `qa`, `qa-only`, `review`, `code-review-checklist`, and `verify-changes` together by default. Choose the narrowest combination required.
- `qa`, `qa-only`, and `review` are vendor/gstack orchestration skills with substantial runtime assumptions. Prefer portable skills unless that environment/workflow is intentionally being used.
- For application UI, prefer `frontend-design` + `frontend-architecture` as needed. Add `ui-styling` only for its concrete stack. Keep `design-review`, `design-shotgun`, and `design-consultation` specialized/opt-in.
- Do not load `frontend-design`, `ui-styling`, `design`, `design-review`, `design-shotgun`, and `design-consultation` as one bundle.

## Front-End Checklist source policy

The cloned source at `/Google Drive/Front-End-Checklist` is retained as the detailed frontend quality corpus.

- Default: load `.agents/skills/frontend-quality/SKILL.md`.
- Deep audit or uncertain rule: consult `.agents/skills/frontend-quality/references/front-end-checklist.md` and then the cloned source only for the relevant category/rule.
- If the Front-End Checklist MCP tools are available in the active environment, use retrieval for exact rules rather than copying all rules into agent context.

## Project isolation

A project profile may require or forbid techniques, but it must not redefine a shared skill as globally mandatory. Shared skills remain reusable across projects.
