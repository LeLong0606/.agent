---
name: find-skill
description: "Invoked when the user is stuck on a problem and wants a skill recommendation. First summarizes the current blocker (from conversation context, project state, and/or the user's argument) and pauses for user confirmation. Then scans locally available skills, and if none fit, searches GitHub for high-star Claude Code skill repos. Presents candidates for the user to review; never installs without explicit user approval."
argument-hint: "[optional: one-line description of the problem]"
license: MIT
---

# /find-skill — Recommend a skill for the current blocker

Use this when the user is stuck and asks for a skill recommendation (either via `/find-skill` or `/find-skill <problem description>`). The goal is to (1) crisply summarize what's blocking them, (2) show candidate skills — local first, GitHub fallback — and (3) let the user decide whether and which to install. **Never auto-install.**

## Step 1 — Summarize the blocker, then pause

Build the summary from whichever signals are available:

- **No argument**: synthesize from the current conversation — recent failures, error messages, what the user has tried, their stated frustration. If the conversation is thin, glance at project state (package.json, README, recent git log, failing tests, build errors) for additional cues.
- **With argument** (`/find-skill <text>`): treat the user's text as the primary signal. Use conversation and project state only as secondary context to sharpen the summary.
- **Both**: user's argument wins on what the blocker *is*; conversation fills in what's been tried.

Present the summary in this shape:

> **Current blocker (please confirm)**
> - Stuck on: <one sentence>
> - Tried so far: <one line, or "nothing obvious">
> - What unblocking enables: <one line>
>
> Confirm / correct / add more?

**Stop here.** Do not proceed to Step 2 until the user confirms or revises. If the user partially rejects or adds context, update the summary and — only if the change is substantive — re-confirm once. Small clarifications don't need another confirm round.

## Step 2 — Scan local skills first

The currently available skills are listed in the conversation's system-reminder (visible to you at invocation). Review that list against the confirmed blocker.

For each plausible match, note:
- skill name
- one line on why it fits
- one line on any gap or caveat (if relevant)

Present the **top 1–3** local matches. If nothing reasonable exists locally, say so explicitly — do not force a bad match. Then proceed to Step 3.

## Step 3 — GitHub search (only if local is insufficient)

Use WebSearch. Try queries in this order, stopping when you have enough signal:

1. `claude-code skill <domain-keyword> site:github.com`
2. `anthropic claude skill <keyword> site:github.com`
3. `<domain-keyword> SKILL.md site:github.com`
4. Plain `<domain> claude code` as a last fallback

Prioritize by GitHub stars. If WebSearch results don't expose star counts, use WebFetch on the top candidates to read the repo page. Filter out:
- repos that aren't Claude Code skills (e.g. Cursor rules, generic prompt collections) — unless nothing else exists, in which case flag them as "needs conversion"
- archived / unmaintained repos (last commit > 1 year ago) unless stars are very high

Present **top 3–5** candidates in this shape:

> | # | Repo | ★ | What it does | Why it fits the blocker |
> |---|------|---|--------------|-------------------------|
> | 1 | owner/name | 420 | ... | ... |

If the search returns nothing credible, say so and suggest the user describe the blocker differently or accept that this may be a gap to write their own skill.

## Step 4 — User picks (or passes)

Ask which candidate (if any) they want to preview. Do not proceed without an explicit pick.

## Step 5 — Preview before install

For the chosen candidate, WebFetch the repo and show:
- Full `SKILL.md` content (summarize only if > ~150 lines, and say so)
- Any install / setup steps from README
- **Security notes**: list any scripts the skill runs, external tools it requires, network calls, or credentials it asks for. Flag anything unusual.

Then ask: **"Install to `~/.claude/skills/<name>/`? (confirm / cancel / pick another)"**

## Step 6 — Install (only on explicit confirmation)

On explicit yes:
- Create `~/.claude/skills/<skill-name>/`
- Write `SKILL.md` and any referenced files (scripts, references, templates) from the repo
- Tell the user: the skill is available as `/<skill-name>` in **new** conversations; the current session won't see it until restart.

Do not run any setup scripts from the installed skill automatically — leave that to the user.

## Hard rules

- **Never skip the Step 1 confirmation pause**, even when the user provides an argument — they may want to add context.
- **Never install without the explicit Step 6 confirmation.**
- **Never recommend more than 5 candidates total.** Short lists force better curation.
- If local skills fully cover the blocker, say so and do not run GitHub search — don't pad the answer.
- If the user's blocker is actually a code bug (not a missing capability), say so plainly; a skill won't fix it.
