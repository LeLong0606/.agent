---
name: frontend-quality
description: Project-neutral frontend implementation and review quality gate distilled from the cloned Front-End Checklist corpus.
version: 2.0.0
source: /Google Drive/Front-End-Checklist
---

# Frontend Quality

Use this skill for frontend implementation, review, debugging, and pre-completion auditing.
It is intentionally compact: do not load hundreds of micro-rules unless a specific issue requires deeper lookup.

Detailed source relationship and escalation guidance live in:

- `.agents/skills/frontend-quality/references/front-end-checklist.md`

## Responsibility boundary

This skill owns **quality**, not every frontend concern.

- Code organization/state/data boundaries → `frontend-architecture`.
- Visual direction/layout/aesthetic decisions → `frontend-design`.
- shadcn/ui, Radix, Tailwind implementation detail → `ui-styling` when applicable.
- React/Next-specific performance → `nextjs-react-expert` when applicable.
- Deep security/SEO/i18n work → add the relevant specialized skill.

Do not load all of those automatically.

## Audit stance

- Prefer fewer, stronger findings over speculative breadth.
- Report an issue only when inspected code, markup, rendered behavior, or repository context supports it.
- Do not infer business intent from an isolated snippet.
- Distinguish defects from preferences and optional enhancements.
- Prioritize critical/high-impact accessibility, security, correctness, performance, and UX issues.
- For a small component/route, prefer the strongest 1–2 supported findings instead of dumping every possible improvement.

## Core coverage

### HTML and structure

- Prefer semantic HTML and native controls.
- Keep IDs unique.
- Use appropriate input and button types.
- Preserve valid heading/list/table semantics.

### Accessibility

- Ensure controls have accessible names and labels.
- Support keyboard navigation and visible focus.
- Use ARIA only when native semantics are insufficient.
- Associate validation errors with fields and avoid color-only error indication.
- Respect reduced-motion preferences for persistent/non-essential motion.

### Responsive and CSS

- Prevent unintended horizontal page overflow.
- Do not disable browser zoom.
- Prefer low-specificity maintainable selectors.
- Avoid unnecessary `!important`.
- Prefer transform/opacity for simple animation when appropriate.

### Images

- Give meaningful content images appropriate alternative text.
- Decorative images may correctly use `alt=""` and/or `aria-hidden="true"`.
- Reserve layout space for meaningful images when layout shift is plausible.
- Use responsive/lazy-loading techniques when they materially help; do not demand them for tiny decorative assets without evidence.

### Forms

- Check label association, input type, button type, validation feedback, accessible errors, and useful autocomplete hints.
- Do not require traditional `action`/`method` when client-side submit handling is explicit and correct.

### Performance

- Look for concrete layout shift, blocking resources, expensive animations, excessive re-rendering, and repeated DOM read/write patterns.
- Avoid theoretical optimization findings without evidence.
- For React/Next-specific optimization, escalate to `nextjs-react-expert` rather than duplicating framework rules here.

### Security

- Check unsafe HTML injection, exposed secrets, insecure resource URLs, unsafe external-link behavior, and risky third-party script loading.

### Metadata / SEO

- Audit page metadata only when the inspected route/file owns metadata.
- In frameworks such as Next.js, consider framework metadata APIs before claiming literal `<head>` tags are missing.

### Testing

- Cover happy path plus relevant loading, empty, failure, keyboard/accessibility, and responsive states.

## Known safe patterns

Do not automatically flag:

- `alt=""` on clearly decorative images.
- Decorative micro-SVGs for missing lazy loading or dimensions without layout-shift evidence.
- React forms with explicit client-side submit handling for missing server `action`/`method`.
- Missing literal meta tags when the framework metadata API owns them.
- Missing table caption when an adjacent visible heading already gives clear context; prioritize actual header association defects.
- Child image dimensions when a stable aspect-ratio wrapper clearly reserves layout space.

## Conflict resolution

- Decorative-image semantics beat generic image-dimension advice unless there is real layout-instability evidence.
- Explicit client-side form handling beats generic server-post form advice.
- Framework metadata APIs beat generic literal-head-tag expectations.
- Evidence beats generic preference.

## Deep-check escalation

Escalate beyond this compact skill when:

- the user requests a comprehensive frontend audit;
- a potential issue is standards-sensitive or ambiguous;
- a critical/high finding needs exact remediation;
- accessibility, security, privacy, SEO, i18n, performance, or testing requires category-specific depth.

Then consult `.agents/skills/frontend-quality/references/front-end-checklist.md` and retrieve only the relevant rule/category from the cloned Front-End-Checklist source. If its MCP retrieval tools are available, prefer exact retrieval over copying the whole corpus into context.

## Finding format

For each real issue provide:

1. Severity.
2. Exact location/evidence.
3. User or operational impact.
4. Concrete fix.
5. Verification method.

If evidence is insufficient, say so instead of manufacturing a finding.
