# Front-End Checklist Reference

## Source relationship

This repository's runtime source of truth is the bundled
`portable-checklist.md` in this reference directory.

The skill was informed by an external Front-End Checklist corpus covering 385 rules, but it has no runtime dependency on that checkout, its location, or its MCP service. Do not add machine-specific source paths. External retrieval may supplement the bundled checklist when available; it must never be required for a cloned `.agent` workspace to function.

## How this repository uses the source

`../SKILL.md` is the compact default runtime skill.
This reference preserves the high-value review policy and tells the agent when to load the bundled detailed checklist.

Do **not** install hundreds of individual checklist micro-skills into `skills/`.

## Source coverage

The source corpus covers:

- HTML
- CSS
- JavaScript
- Performance
- Accessibility
- SEO
- Security
- Images
- Testing
- Privacy
- Internationalization

## Conservative audit policy

Preserve these source principles:

- Prefer fewer, stronger findings over speculative breadth.
- Report only issues directly supported by inspected code/markup/rendered behavior/context.
- Do not infer business requirements from isolated snippets.
- For small component/route audits, prefer the strongest 1–2 supported findings.
- Do not elevate low-confidence preference tweaks into defects.
- Explain uncertainty rather than overstating.

## High-value safe patterns

Treat these as context-sensitive safe patterns unless evidence shows a real defect:

- Decorative image: `alt=""`, optionally with `aria-hidden="true"`.
- Tiny decorative SVGs/favicons without explicit dimensions when layout stability is already guaranteed.
- Client-handled React forms with an explicit `onSubmit` and no traditional server `action`/`method`.
- Next.js metadata APIs (`metadata`, `viewport`, `generateMetadata`) instead of literal `<head>` markup.
- Preview-card images/favicons using empty alt when nearby visible text already names the destination.
- Aspect-ratio wrappers that reserve stable media space even when the child image omits explicit dimensions.
- A visible adjacent heading that already explains a simple table; prioritize actual header associations before demanding a caption.
- Pseudo-element focus rings when they are visibly reliable, correctly anchored, and not clipped.

## Conflict resolution

When generic rules conflict:

1. Specific semantic/context evidence wins over generic checklist advice.
2. Decorative-image guidance wins over generic dimensions guidance unless real layout instability is shown.
3. Explicit client-side form behavior wins over generic server-form expectations.
4. Framework metadata ownership wins over assumptions based on missing literal meta tags.
5. Concrete user harm/performance evidence wins over hypothetical optimization.

## Category routing

Use only the additional skill that contributes unique depth:

| Concern | Default | Add when needed |
|---|---|---|
| Structure/HTML/a11y/forms/images/CSS | `frontend-quality` | Retrieve focused Front-End-Checklist rule/category |
| Frontend organization/state/data | `frontend-architecture` | — |
| Visual design | `frontend-design` | `ui-styling` for shadcn/Tailwind implementation |
| React/Next performance | `frontend-quality` | `nextjs-react-expert` |
| Deep frontend security | `frontend-quality` | `frontend-security-defense` |
| SEO-specific project work | `frontend-quality` | `seo-fundamentals` |
| Localization | `frontend-quality` | `i18n-localization` + project ownership rules |
| Browser/E2E proof | `frontend-quality` | `webapp-testing` |
| Vercel Web Interface Guidelines specifically | `frontend-quality` | `web-design-guidelines` opt-in |

## Deep retrieval workflow

When compatible external checklist retrieval tooling is available:

1. Use focused code review first for inspected code.
2. Search rules before giving standards-sensitive accessibility/performance/SEO/security/images/privacy/i18n/testing recommendations.
3. Retrieve the exact rule for exact remediation.
4. Use full workflow/checklist retrieval only for broad audits.
5. Audit a public URL only when rendered-page evidence is useful.

When MCP tooling is not available, read the relevant category in
`portable-checklist.md` in this reference directory.

## Evaluation standard

A useful frontend finding should include:

- severity/priority;
- exact file/route/selector/snippet or rendered evidence;
- why it matters;
- concrete fix;
- verification;
- exceptions/uncertainty when relevant.

The goal is not to maximize the number of findings. The goal is to maximize supported, actionable findings with low false-positive risk.
