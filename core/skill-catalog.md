# Shared Skill Catalog

This registry controls routing priority without rewriting or deleting vendor skill sources.

## Status meanings

- **PRIMARY** — preferred default for its concern.
- **SUPPORTING** — add only when its narrower capability is materially needed.
- **SPECIALIZED** — valid, but opt-in because it is stack-, workflow-, vendor-, or environment-specific.
- **COMPATIBILITY** — retained so old references keep working; route to the replacement for new work.

## Debugging

| Skill | Status | Routing note |
|---|---|---|
| `systemic-debugging` | PRIMARY | Fast path + cross-layer/timing/lifecycle root-cause investigation. |
| `investigate` | SUPPORTING | Evidence collection and focused investigation. |
| `systematic-debugging` | COMPATIBILITY | Alias to `systemic-debugging`; do not load both. |

## Generic review, QA, and verification

| Skill | Status | Routing note |
|---|---|---|
| `verify-changes` | PRIMARY | Prove behavior by execution; default completion evidence. |
| `code-review-checklist` | PRIMARY | Portable generic correctness/security/code-quality review. |
| `lint-and-validate` | SUPPORTING | Lint/type/schema validation when applicable. |
| `testing-patterns` | SUPPORTING | Test strategy and test design. |
| `tdd-workflow` | SUPPORTING | Use when test-first implementation is desired. |
| `webapp-testing` | SUPPORTING | Browser/E2E verification. |
| `checking-minor-errors` | SUPPORTING | Optional final lightweight pass. |
| `qa` | SPECIALIZED | gstack test-fix-verify orchestration; large vendor runtime/preamble. |
| `qa-only` | SPECIALIZED | gstack report-only QA orchestration. |
| `review` | SPECIALIZED | gstack pre-landing PR workflow. |

## Frontend engineering

| Skill | Status | Routing note |
|---|---|---|
| `frontend-architecture` | PRIMARY | UI/logic/data/type boundaries, state tiers, framework structure. |
| `frontend-quality` | PRIMARY | Default frontend quality gate, distilled from Front-End-Checklist. |
| `frontend-design` | PRIMARY | Visual/web UI design decisions and implementation direction. |
| `nextjs-react-expert` | SUPPORTING | React/Next performance and framework-specific optimization. |
| `ui-styling` | SUPPORTING | shadcn/ui + Radix + Tailwind implementation patterns. |
| `frontend-security-defense` | SUPPORTING | Deep frontend security review. |
| `i18n-localization` | SUPPORTING | Localization implementation; ownership comes from project profile. |
| `seo-fundamentals` | SUPPORTING | SEO-specific work beyond the generic quality gate. |
| `web-design-guidelines` | SPECIALIZED | Use when the Vercel Web Interface Guidelines are explicitly requested or uniquely useful. |

## Design and visual creation

| Skill | Status | Routing note |
|---|---|---|
| `design` | PRIMARY | Brand/logo/CIP/banner/social/slides and non-app visual artifact routing. Not the default application-UI skill. |
| `design-system` | SUPPORTING | Tokens/specs/design-system implementation. |
| `brand` / `brand-guidelines` | SUPPORTING | Brand-specific work. |
| `design-review` | SPECIALIZED | gstack visual QA/fix workflow. |
| `design-shotgun` | SPECIALIZED | gstack multi-variant exploration workflow. |
| `design-consultation` | SPECIALIZED | gstack DESIGN.md / design-system discovery workflow. |
| `design-html` | SPECIALIZED | gstack/Pretext finalization with substantial runtime assumptions. |

## Backend and architecture

| Skill | Status | Routing note |
|---|---|---|
| `architecture` | PRIMARY | System boundaries and architectural decisions. |
| `api-patterns` | PRIMARY | HTTP/API contracts and patterns. |
| `database-design` | PRIMARY | Schema/query/transaction/data design. |
| `dotnet-clean-arch-vsa` | PRIMARY | .NET Clean Architecture/VSA/CQRS projects. |
| `clean-code` | SUPPORTING | Source-quality pass when code is being changed. |
| `backend-security-defense` | SUPPORTING | Defensive backend security review. |

## Operations

| Skill | Status | Routing note |
|---|---|---|
| `deployment-procedures` | PRIMARY | Deployment workflow and rollout concerns. |
| `server-management` | SUPPORTING | Host/server administration. |
| `bash-linux` | SUPPORTING | Linux shell/operations. |
| `powershell-windows` | SUPPORTING | Windows/PowerShell operations. |
| `coordinator-mode` | SPECIALIZED | Multi-domain orchestration only when needed. |
| `parallel-agents` | SPECIALIZED | Parallelizable work with non-overlapping writes. |

## Front-End Checklist ownership

The cloned `/Google Drive/Front-End-Checklist` repository is a source corpus, not a set of 385 default runtime skills.

- `.agents/skills/frontend-quality/SKILL.md` is the compact default entry point.
- `.agents/skills/frontend-quality/references/front-end-checklist.md` records the distilled policy and source relationship.
- Individual cloned checklist skills/rules are retrieved only when a focused audit requires them.

## Migration rule

Do not delete or rewrite vendor skill sources solely because they are SPECIALIZED or COMPATIBILITY. Routing status is enough to keep normal context small while preserving rollback and future reuse.
