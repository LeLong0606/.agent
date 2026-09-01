---
name: antigravity-walkthrough-handoff
description: Guidance for locating and reading Antigravity IDE's "brain" artifacts (walkthrough.md, implementation_plan.md, task.md) to continue work that Antigravity previously started. Use this whenever asked to "continue Antigravity's work", "pick up where Antigravity left off", "read the walkthrough", or given a path/filename under a `.gemini\antigravity*\brain\` folder. Critical when the project has MANY brain conversation folders and MANY walkthrough files — this skill defines how to find the correct one instead of reading all of them. Do NOT use this for normal project code reading — only for consuming Antigravity's own session artifacts.
---

# Antigravity Walkthrough Handoff

Guidance for reading Antigravity IDE/CLI's session artifacts so another agent (e.g. Codex) can accurately continue previously-started work, without wasting tokens scanning every conversation folder.

## Background: what the `brain/` folder actually contains

Antigravity stores one folder per conversation (task/session), named by its Conversation ID (a UUID). Depending on which Antigravity product was used, the base path differs:

| Product | Base path (Windows) |
|---|---|
| Antigravity IDE | `%USERPROFILE%\.gemini\antigravity-ide\brain\` |
| Antigravity 2.0 (Agent Manager) | `%USERPROFILE%\.gemini\antigravity\brain\` |
| Antigravity CLI | `%USERPROFILE%\.gemini\antigravity-cli\brain\` |

**These three brain folders are separate — they are not merged.** If a walkthrough can't be found under the path you were given, check the other two variants before concluding it doesn't exist.

Inside each conversation folder (`brain\<conversation-id>\`), you may find:
- `walkthrough.md` (or a topic-suffixed variant like `walkthrough_frontend_security.md`) — a summary of what was actually done and changed.
- `implementation_plan.md` — the plan that was proposed/approved before execution.
- `task.md` — a checklist of the plan's steps, which may show some steps as incomplete.
- `.system_generated/logs/` — raw JSONL transcripts (full conversation history). Only read this as a last resort — it is large and expensive; the markdown artifacts above are the intended summary layer.

## When you're already given a full file path

If the path is already fully specified (e.g. `...\brain\aaee20ab-6090-4eb4-b78d-687c4972d3a0\walkthrough_frontend_security.md`), skip straight to **"What to read and in what order"** below — no search needed.

## When you only have a topic, or are told to "continue Antigravity's work" without a specific path

Do NOT read every walkthrough across every brain folder — with many conversations and many walkthroughs, that burns a large amount of tokens for little benefit. Instead:

1. **List conversation folders sorted by most recently modified first.** The most recent conversation is very likely the one referenced, since Antigravity conversations are typically sequential per topic area.
   ```powershell
   Get-ChildItem "$env:USERPROFILE\.gemini\antigravity-ide\brain" -Directory | Sort-Object LastWriteTime -Descending
   ```
   ```bash
   ls -lt ~/.gemini/antigravity-ide/brain/
   ```
2. **Search filenames for the topic keyword** given by the user (e.g. "security", "frontend", "notification") across the candidate folders, rather than opening each one blindly:
   ```powershell
   Get-ChildItem "$env:USERPROFILE\.gemini\antigravity-ide\brain" -Recurse -Filter "walkthrough*.md" | Where-Object { $_.Name -match "security" }
   ```
   ```bash
   find ~/.gemini/antigravity-ide/brain -iname "walkthrough*<topic>*.md"
   ```
3. **If more than one candidate matches** (same topic keyword appears in multiple conversation folders), do not guess — briefly list the candidates (folder name + last-modified date) and ask which one is correct. Picking the wrong conversation and building on stale/unrelated context is more expensive than one clarifying question.
4. **If nothing matches the topic keyword**, widen the search to `implementation_plan.md` and `task.md` filenames/content too — sometimes the topic is only named in the plan, not in the walkthrough filename itself.

## What to read, and in what order

1. **`walkthrough.md` (or `walkthrough_<topic>.md`) first** — this is the intended summary of what was actually completed. It usually answers "what changed and why" without needing anything else.
2. **Only if the walkthrough is incomplete, ambiguous, or the task looks unfinished**, also read `task.md` in the same folder — it shows which planned steps were actually checked off versus left pending. This tells you exactly where to resume, instead of re-deriving it from the code.
3. **Only if you need the original reasoning/scope** (e.g. to understand why a particular approach was chosen), read `implementation_plan.md`.
4. **Avoid the raw JSONL transcript** under `.system_generated/logs/` unless the three markdown artifacts above genuinely don't answer what you need — it is unstructured and far more expensive to parse.

## What to extract before writing any new code

From the walkthrough (and task.md if needed), extract explicitly:
- **What was completed** — which files were changed, which feature/fix was delivered.
- **What was left pending or explicitly deferred** — don't assume "walkthrough exists" means "fully done"; `task.md` may show unchecked items.
- **Any decisions or constraints mentioned** (e.g. "chose Dapper over EF Core because...", "left X for a follow-up conversation") — these must be respected when continuing, not silently re-decided.
- **Any known issues or follow-ups the walkthrough explicitly flags.**

## Continuation etiquette

- Before making any change, restate a short summary (2–4 lines) of what Antigravity already did, based on the walkthrough — this lets the person confirm you picked up the right context before you spend effort building on it.
- Follow the same project conventions Antigravity used (naming, folder structure, patterns) — if the project has its own architecture skill (e.g. a `.NET Clean Architecture + VSA` skill), that skill is still the source of truth for *how* to write the code; this skill only tells you *where to find what was already done*.
- Do not silently redo work that the walkthrough shows was already completed — if something looks done but appears broken, say so explicitly rather than quietly rewriting it.

## Common mistakes to avoid

| # | Mistake | Correct approach |
|---|---|---|
| 1 | Reading every walkthrough across every brain folder to "be thorough" | Narrow by recency + topic keyword first; only widen the search if nothing matches |
| 2 | Assuming `.gemini\antigravity\`, `antigravity-ide\`, and `antigravity-cli\` share the same brain folder | Treat them as separate; check the correct product-specific path |
| 3 | Treating `walkthrough.md` as proof the entire plan was finished | Cross-check `task.md` for unchecked/pending steps before assuming completion |
| 4 | Parsing the raw `.system_generated/logs/` JSONL transcript by default | Use it only as a last resort, after the markdown artifacts fail to answer the question |
| 5 | Picking a conversation folder to read without confirming when multiple candidates match the same topic | Ask which conversation is correct rather than guessing |
| 6 | Re-deciding an architectural choice that the `implementation_plan.md` already explains the reasoning for | Read the stated reasoning first and preserve it unless explicitly asked to change it |
