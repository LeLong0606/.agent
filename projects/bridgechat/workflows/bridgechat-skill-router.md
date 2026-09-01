---
name: bridgechat-skill-router
description: Select the smallest effective BridgeChat skill set for backend, frontend, distributed, and debugging work.
version: 3.1.0
artifact_outputs: selected-skills, execution-strategy, quality-gates
---

# BridgeChat skill router

Run `bridgechat-request-intake` first. Follow `.agents/core/skill-routing.md` and consult `.agents/core/skill-catalog.md` when skills overlap. Read every selected `SKILL.md` completely, but do not load the whole catalog.

Always use BridgeChat brain context and `bridgechat-text-integrity` where required by the project workflow. Use `verify-changes` before completion. Add `clean-code`, `lint-and-validate`, or `checking-minor-errors` only when they contribute a concrete source-quality or verification step.

| Signal | Required routing |
|---|---|
| New/ambiguous feature | `brainstorming`, `architecture`; add `plan-writing` when planning depth is needed |
| .NET CQRS/VSA | `dotnet-clean-arch-vsa`; add `api-patterns` for HTTP contracts |
| SQL/schema/transaction | `database-design` |
| Multiple services/events/Saga | `architecture`, `bridgechat-microservice-orchestration`; add `coordinator-mode` only when safe partitioning helps |
| Auth/PII/upload | defensive security skill first (`backend-security-defense` / `frontend-security-defense` / `vulnerability-scanner`); `red-team-tactics` only when explicitly appropriate |
| React component/state/data structure | `frontend-architecture` |
| Visible UI quality/accessibility | `frontend-quality`; add `frontend-design` for visual-design decisions |
| Tailwind/shadcn/Radix implementation detail | `ui-styling` |
| React/Next performance/framework behavior | `nextjs-react-expert` |
| Vercel Web Interface Guidelines specifically | `web-design-guidelines` opt-in |
| Frontend translations | `i18n-localization`; `bridgechatwebreact/public/locales/**` only |
| Backend localization | `i18n-localization`; `BridgeChat.SharedLibraries/Core.Localization/Resources/*.json` only |
| Defect/4xx/5xx/race/intermittent issue | `systemic-debugging`; add `investigate` for evidence gathering |
| Test strategy | `testing-patterns` |
| Test-first implementation | `tdd-workflow` |
| Browser/E2E proof | `webapp-testing` |
| Completion proof | `verify-changes`; add `lint-and-validate` where applicable |

For BridgeChat frontend work, the generic `.agents/workflows/frontend-quality-gate.md` is the default quality gate and uses the cloned Front-End-Checklist as its detailed source corpus.

Research may be parallel. The main agent must synthesize ownership/contracts before assigning writes. Never let workers edit the same file concurrently. Do not commit, push, deploy, reset data, or delete volumes unless explicitly requested.
