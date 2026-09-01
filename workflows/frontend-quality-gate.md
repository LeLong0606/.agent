# Frontend Quality Gate

Run this workflow before declaring frontend/UI work complete.
The default quality source is `.agents/skills/frontend-quality/SKILL.md`, distilled from the cloned `/Google Drive/Front-End-Checklist` corpus.

## 1. Establish scope

Identify the changed routes/components/styles and determine which concerns actually apply.
Do not audit unrelated pages merely because they exist.

## 2. Functional verification

Verify requested behavior first, including relevant loading, empty, error, disabled, success, responsive, and keyboard states.
A quality audit does not compensate for missing requested functionality.

## 3. Quality review

Use `.agents/skills/frontend-quality/SKILL.md` and review applicable areas:

- semantics/HTML
- accessibility/keyboard/focus
- responsive/CSS
- forms
- images/layout shift
- JavaScript/rendering/performance
- security
- metadata/SEO when route-owned
- tests

Do not automatically load `frontend-design`, `ui-styling`, `nextjs-react-expert`, `web-design-guidelines`, or other frontend skills. Add one only when it contributes unique depth to the actual change.

## 4. False-positive filter

Before reporting or fixing a finding:

1. Check the known-safe patterns in `frontend-quality`.
2. Confirm the inspected file/route actually owns the concern.
3. Remove preference-only or context-free findings.
4. Prefer silence over weak nitpicks.

For standards-sensitive or ambiguous findings, consult `.agents/skills/frontend-quality/references/front-end-checklist.md` and retrieve only the relevant source rule/category.

## 5. Fix and re-verify

Fix critical/high supported findings within task scope and rerun the narrowest available lint/type-check/build/tests plus focused UI/browser verification.

Use `verify-changes` for execution evidence. Add `webapp-testing` when browser/E2E proof is needed.

## 6. Completion report

Report:

- what changed;
- what was verified and how;
- remaining supported findings, if any;
- anything that could not be verified.

For BridgeChat, this gate supplements rather than replaces BridgeChat verification and text-integrity workflows.
