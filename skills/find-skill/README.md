# find-skill

A Claude Code skill that recommends *other* skills when you're stuck.

Trigger it with `/find-skill` (or `/find-skill <one-line problem description>`) and Claude will:

1. **Summarize** what's actually blocking you — pulled from the conversation, the project state, your argument, or all three — and pause for you to confirm or correct.
2. **Scan your locally installed skills** for a match, and present the top 1–3 with reasoning.
3. **Fall back to GitHub** only if nothing local fits — searching for high-star Claude Code skill repos, filtering out archived and non-native ones.
4. **Present candidates as a short table** (star count, description, why it fits) so you can compare at a glance.
5. **Preview the chosen skill's `SKILL.md`** plus any security-relevant notes before anything gets installed.
6. **Install only on your explicit confirmation** — the skill will never write to `~/.claude/skills/` on its own.

## Why this exists

Claude already has every installed skill in its context on every turn, but in practice it often forgets to reach for them when you hit a wall. And when you *don't* have a matching skill, there's no good workflow for discovering one without breaking your flow to go googling.

`/find-skill` forces a deliberate pause — *what are you actually stuck on?* — and then does the search for you, with the user firmly in the loop on what gets installed.

## Installation

Clone into your user-level skills directory:

```bash
git clone https://github.com/Emily27-alt/find-skill.git ~/.claude/skills/find-skill
```

Or manually drop `SKILL.md` into `~/.claude/skills/find-skill/SKILL.md`.

The skill becomes available as `/find-skill` in **new** Claude Code conversations. Existing sessions will not see it until they restart.

## Usage

```text
/find-skill
```

With no argument, Claude infers the blocker from the current conversation (recent errors, what you've tried, your stated frustration). Good for mid-session use.

```text
/find-skill I can't get shadcn to coexist with our existing Tailwind config
```

With an argument, your description becomes the primary signal; conversation and project state act as secondary context. Good for fresh sessions or when the chat history is noisy.

## Flow at a glance

```
┌──────────────────────────────────────────┐
│ 1. Summarize blocker ── pause ── confirm │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ 2. Scan local skills (top 1–3)            │
└──────────────────────────────────────────┘
                    ↓  (only if local is insufficient)
┌──────────────────────────────────────────┐
│ 3. GitHub search by stars (top 3–5)       │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ 4. User picks one (or passes)             │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ 5. Preview SKILL.md + security notes      │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ 6. Install on explicit confirmation only  │
└──────────────────────────────────────────┘
```

## Design rules (enforced inside the skill)

- **Never skip the Step 1 confirmation pause.** Even when you pass an argument, you still get to correct the summary before the search runs.
- **Never install without explicit confirmation at Step 6.** No silent writes to `~/.claude/skills/`.
- **Never recommend more than 5 candidates total.** Short lists force better curation.
- **No padding.** If local skills already cover the blocker, the GitHub search is skipped.
- **No false promises.** If the blocker is actually a code bug rather than a missing capability, the skill says so — a new skill won't fix a broken function.

## Security notes

Installed skills are markdown-based instructions that Claude follows during your sessions. Treat them the way you'd treat a script you're about to run:

- Step 5 always shows you the full `SKILL.md` content before installation.
- Any referenced scripts, external tools, or credentials are called out explicitly.
- Setup scripts from installed skills are **never** run automatically — that's on you.

## Roadmap ideas

- Optional `--local-only` flag to skip GitHub search entirely
- Support for namespaced skills (e.g. `ckm:banner-design`)
- Cache recent GitHub searches so repeated lookups are faster

## License

MIT. See [LICENSE](./LICENSE).

## Contributing

Issues and PRs welcome. This skill is deliberately small — the goal is a reliable discovery loop, not a full package manager. Keep proposals aligned with that scope.
