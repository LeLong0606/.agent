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
| `impeccable` | SPECIALIZED | Comprehensive interface design/polish workflow with detectors and live tooling; use for deliberate visual-quality passes. |
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

## Browser automation and research

| Skill | Status | Routing note |
|---|---|---|
| `agent-browser` | SPECIALIZED | Browser CLI workflow; use its focused companion skill for automation, debugging, E2E, scraping, iOS, or visual work. |
| `agent-browser-automate` / `agent-browser-e2e` | SPECIALIZED | Browser automation and E2E flows when the agent-browser runtime is available. |
| `agent-browser-debug` / `agent-browser-visual` | SPECIALIZED | Browser diagnosis and visual evidence. |
| `agent-browser-scrape` | SPECIALIZED | Structured browser extraction when permitted and appropriate. |
| `last30days` | SPECIALIZED | Time-sensitive multi-source research with its own setup/runtime requirements. |

## Motion and media

| Skill | Status | Routing note |
|---|---|---|
| `animate` | SUPPORTING | General interface motion guidance when animation is part of the requested experience. |
| `gsap-*` | SPECIALIZED | Load only the matching GSAP concern: setup, scroll, text, SVG, canvas, interaction, optimization, test, or VFX. |
| `motion-doctrine` / `seam-craft` / `cut-the-curve` | SPECIALIZED | Focused motion-system and transition craft. |
| `captions-overlay` / `changelog-video` / `remotion-motion-graphics` | SPECIALIZED | Video/caption/motion-graphics production with the required media runtime. |

## Product and marketing

The imported marketing skills are opt-in. Select one narrow capability such as `marketing-plan`, `product-marketing`, `analytics`, `seo-audit`, `copywriting`, `pricing`, `launch`, `onboarding`, or `churn-prevention`; do not load the full marketing collection.

## Imported workflow suites

- `Claude-Skills` planning/review/execution skills are SPECIALIZED. Prefer existing primary workspace workflows when they cover the same concern.
- `ponytail-*` skills are SPECIALIZED codebase-improvement workflows; load only when explicitly useful.
- `humanizer`, `graphify`, and `i-have-adhd` are opt-in transformations/work styles, not default engineering companions.

## Scoped implementation workflows

| Skill | Status | Routing note |
|---|---|---|
| `surgical-patch` | SUPPORTING | Narrow bug or small behavior change with regression proof and preserved surrounding behavior. |
| `safe-refactor` | SUPPORTING | Behavior-preserving extraction, consolidation, ownership move, or cleanup. |
| `migration` | SUPPORTING | Compatibility-safe schema, data, API, protocol, configuration, or dependency transition. |
| `lean-build` | SPECIALIZED | Feature slices with high overbuilding risk and an explicit stop condition. |
| `investigate-first` | COMPATIBILITY | Evidence-ranked investigation style; prefer `systemic-debugging` plus `investigate` for normal routing. |
| `verify-and-stop` | COMPATIBILITY | Narrow validation-only workflow; prefer `verify-changes` unless its strict stop boundary is specifically useful. |
| `caveman-explore` | SPECIALIZED | Read-only compressed repository exploration after direct search is insufficient. |

## HyperFrames media suite

`hyperframes` is the specialized entry point for HyperFrames video or motion-composition work. Load only its routed companion, such as `product-launch-video`, `pr-to-video`, `faceless-explainer`, `embedded-captions`, `talking-head-recut`, `music-to-video`, `slideshow`, `motion-graphics`, `hyperframes-animation`, `hyperframes-audio`, `media-use`, or `remotion-to-hyperframes`. Do not load the full suite together.

## Upstream synchronization

Source repositories and selection decisions live in `sources/skill-sources.json`.
All installed skill payloads are copied into `skills/` and work without the upstream repositories. After updating optional upstream clones, run `scripts/sync-skill-sources.ps1 -Mode Audit -SourceRoot <path-to-clones>`, then use `-Mode Sync` with the same source root to import only new managed skills. `AGENT_SKILL_SOURCE_ROOT` may provide that path. Existing skills remain review-gated so local and BridgeChat adaptations are not overwritten.

## Front-End Checklist ownership

The Front-End Checklist material is distilled into a portable local corpus, not installed as hundreds of default runtime skills.

- `skills/frontend-quality/SKILL.md` is the compact default entry point.
- `skills/frontend-quality/references/front-end-checklist.md` records the distilled policy and source relationship.
- `skills/frontend-quality/references/portable-checklist.md` provides the standalone detailed fallback.
- `skills/frontend-quality/references/application-ui-checklist.md` adds focused quality checks for API-driven, realtime, optimistic, upload, and chat interfaces.
- Individual cloned checklist skills/rules are retrieved only when a focused audit requires them.

## Migration rule

Do not delete or rewrite vendor skill sources solely because they are SPECIALIZED or COMPATIBILITY. Routing status is enough to keep normal context small while preserving rollback and future reuse.
