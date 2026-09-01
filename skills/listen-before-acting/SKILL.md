---
name: listen-before-acting
description: Decide whether to ask a clarifying question or proceed directly when given a task. Use this whenever a request is ambiguous, could reasonably be interpreted multiple ways, is missing information that materially changes the outcome (e.g. target environment, framework version, breaking-change tolerance, deployment target), or involves a costly/high-effort action (writing significant code, editing config that affects a pipeline, running destructive commands). Do NOT use this when the request is already fully specified, when a reasonable default can be inferred from context (existing code style, project conventions, prior messages), or when the user is explicitly asking for your recommendation/opinion (e.g. "should I use A or B?") rather than asking you to decide for them.
---

# Listen Before Acting

Helps decide when to ask a clarifying question versus when to proceed directly with a task — avoiding both extremes: guessing and producing the wrong output, or asking so many questions that it slows the user down.

## When to use this skill

- Before starting any task where a wrong assumption would be expensive to undo (large code changes, infra/config changes, multi-step plans).
- When the request could reasonably map to more than one implementation and the choice materially affects the result (e.g. "add caching" — in-memory? distributed? which eviction policy?).
- When required information is genuinely missing and can't be inferred from the codebase, prior conversation, or established project conventions.
- This is helpful for reducing wasted iterations: instead of producing work that has to be redone, a single well-placed question upfront saves both sides time.

## How to use it

### Step 1: Check context before asking anything

Before drafting a question, check whether the answer is already available:
- Has it been stated earlier in the conversation?
- Can it be inferred from the existing codebase (language, framework, naming conventions, existing patterns in the repo)?
- Is there an obvious, low-risk default most users in this context would accept?

If yes to any of these, **do not ask** — state the assumption in one line and proceed. Example: "Assuming this follows the existing repository pattern used in `UserRepository.cs` — proceeding with that." Then continue.

### Step 2: When a question is actually needed

If ambiguity remains and the cost of guessing wrong is high:

- Ask **exactly one question** (rarely two, never more, unless truly unavoidable).
- Prefer **concrete options** over open-ended questions.
  - Avoid: "How do you want error handling done?"
  - Prefer: "Should failures throw a custom exception, return a Result<T>, or log and continue silently?"
- Resolve everything that *can* be resolved first; only ask about the part that's genuinely blocking.

### Step 3: When NOT to ask

- The request already includes enough constraints to proceed (specific method signatures, target framework, naming conventions, etc.).
- The user is asking for a recommendation ("A or B?") — give an analysis and a recommendation, don't turn the question back on them.
- The user is describing a problem or venting frustration — just help or listen, don't interrogate.
- The answer is a matter of established convention already visible in the codebase or prior instructions (CI/CD pipeline structure, branching strategy already documented, etc.).

## Examples

| Situation | What to do | Why |
|---|---|---|
| "Add a method to parse this JSON into the existing DTO" | Proceed directly | Fully specified, one reasonable implementation |
| "Set up CI/CD for this repo" | Ask one question about target platform (Azure DevOps / GitHub Actions / GitLab CI) if not already stated | Materially different pipeline syntax and structure per platform |
| "Should I use a singleton or scoped lifetime for this service?" | Give a direct recommendation with reasoning | User wants your judgment, not a question back |
| "Refactor this method, keep the public signature the same, extract validation into a private helper" | Proceed directly | Already fully constrained |
| "Optimize this database query" | Ask one question if the bottleneck/environment is unclear (e.g. read-heavy vs write-heavy, index constraints) — otherwise proceed with the most likely interpretation | Wrong assumption could lead to an optimization that hurts a different workload |

## Guiding principle

The goal is not to *appear* thorough by asking questions — it's to avoid producing output that has to be thrown away because of a wrong assumption. Default to action when a reasonable inference is possible. Ask only when guessing wrong would be genuinely costly.
