# Multi-Project Agent Router

This `.agents` workspace is a reusable engineering system for multiple projects. The root is project-neutral; project-specific architecture, workflows, conventions, and memory belong under `.agents/projects/<project>/`.

## Routing Order

For every engineering request:

1. Identify the active project from the user's wording, repository/workspace name, paths, or project context.
2. Load `.agents/core/engineering-rules.md`.
3. Load `.agents/core/skill-routing.md` to select the smallest useful skill set.
4. If a matching project profile exists, load `.agents/projects/<project>/AGENTS.md` before implementation.
5. Execute the project workflow chain when defined; otherwise use a generic workflow.
6. Before completion, run the applicable quality gate and verification steps.

## Project Profiles

### BridgeChat

When the request concerns BridgeChat, `bridgechatwebreact`, `BridgeChat.*`, or its services, load `.agents/projects/bridgechat/AGENTS.md`.

BridgeChat-specific rules override generic rules where they intentionally define stricter architecture, localization, API, encoding, or workflow constraints.

## Generic Frontend Quality

For frontend implementation, review, debugging, or UI integration, use `.agents/skills/frontend-quality/SKILL.md` and `.agents/workflows/frontend-quality-gate.md` when relevant.

## Generic Workflows

For projects without a profile, start with `workflows/request-intake.md` and route to:

- Feature delivery: `workflows/build-feature.md`
- UI delivery: `workflows/build-ui.md`
- Defect fixing: `workflows/fix-error.md`
- Behavior-preserving refactor: `workflows/safe-refactor.md`
- Schema/data/API/protocol/dependency transition: `workflows/migration.md`
- Verification/review: `workflows/verify.md`
- Video, motion, slideshow, or media production: `workflows/media-production.md`

Natural-language examples for all shared and BridgeChat workflows are maintained in `workflows/natural-language-triggers.md`.

## Skill Selection Policy

- Skills are a shared library unless a project profile explicitly owns them.
- When importing a new skill or corpus, first extract only the reusable guidance into `skills/`, `core/`, or `workflows/`.
- Put BridgeChat-specific application, architecture, localization, contract, verification, and orchestration rules only under `projects/bridgechat/`.
- Shared skills and workflows must remain usable without loading a BridgeChat project profile.
- BridgeChat workflows may compose and specialize shared skills; they must not push BridgeChat assumptions back into the shared layer.
- Do not load the full skill catalog.
- Prefer one primary skill per concern and add supporting skills only when they produce a distinct decision or verification step.
- Do not move framework/language skills into a project simply because that project currently uses them.
- Project-specific workflow files belong under `.agents/projects/<project>/workflows/`.

## Rule Precedence

1. Explicit current user instruction.
2. Active project profile under `.agents/projects/<project>/`.
3. Generic core rules under `.agents/core/`.
4. Selected skill/workflow guidance.
5. General best practices.

Do not silently mix conventions from one project into another.
