---
name: systemic-debugging
description: A two-phase methodology for debugging issues that span multiple layers or services (frontend to backend to microservices), especially bugs that are timing-dependent, intermittent, silent (no exception thrown), or only reproducible under a specific sequence of user actions. Use this whenever a bug does NOT have a single clear stack trace pointing to one line of code — for example "data disappears under some condition", "works for user A but not user B", "only fails after logout/login", "message lost with no error logged". Do NOT use the full Phase 2 investigation for simple bugs with a clear error message and stack trace — those should be fixed directly. This skill is technology- and project-agnostic; pair it with any project-specific architecture/naming-convention skill to speed up file location during Phase 1.
---

# Systemic & Cross-Service Debugging

A methodology for debugging problems whose root cause is not a single wrong line of code, but a **mismatch between components across time, layers, or domains**. This is common in distributed systems: a frontend talking to several backend services, background jobs, caches, and message queues that all interact indirectly.

## Core principle: two phases, not one strategy for everything

Most debugging guidance optimizes for speed (minimize tokens/time, narrow down fast). That works for simple bugs but **actively fails** on systemic bugs — narrowing down too aggressively on a bug that spans multiple domains just produces a wrong, overconfident fix. This skill defines two distinct phases and clear rules for switching between them.

| | Phase 1 — Fast Path | Phase 2 — Root Cause Investigation |
|---|---|---|
| **Use when** | Clear error, stack trace, or status code points to a specific place | No single clear failure point; intermittent, timing-dependent, or "silently" wrong behavior |
| **Approach** | Narrow down fast, read the minimum necessary | Deliberately widen scope: trace an entity's full lifecycle across layers/domains |
| **Goal** | Fix the one broken thing | Find the structural/architectural gap that produced the symptom |

**Never force Phase 1's narrowing discipline onto a Phase 2 problem** — a bug that is a gap *between* two correct-looking functions cannot be found by reading either function in isolation, no matter how carefully.

## Phase 1 — Fast Path

1. Capture the exact symptom first: error message, HTTP status code, response body, or (if unavailable) the precise observable behavior.
2. If the system has any form of request tracing (correlation ID, trace ID, request ID), use it to filter logs to the exact failing request — never read logs unfiltered.
3. If a project-specific skill defines naming/routing conventions, use it to jump directly to the suspected file instead of browsing the folder tree.
4. Read only the files most likely responsible, in priority order: the code that directly produced the error first, its immediate dependency second — not the whole surrounding module.
5. Reproduce and verify the fix using existing tooling (an existing test, an existing API collection/request) instead of manually reconstructing the request from scratch.

## Escalation triggers — switch to Phase 2 immediately when any of these are true

- Fast Path has been attempted **twice** without finding the cause — do not attempt a third narrow pass; escalate.
- The bug does not reproduce consistently, or only reproduces under a specific order of actions across multiple users/sessions.
- No exception or error was logged anywhere, yet the outcome is wrong (a "silent" failure).
- The symptom involves data that is supposed to persist or be shared, but disappears, is stale, or is missing for some users/records and not others.
- The bug only appears after a state transition happens elsewhere in the system (logout/login, another user's action, a background job run, a cache eviction).

## Phase 2 — Root Cause Investigation

### Technique 1: Lifecycle / Timeline Tracing

For any bug involving a stateful entity (a token, a key, a session, a cached value, a queued message), stop looking at the single moment it failed and instead reconstruct its **entire lifecycle**:

- When/where is it **created**?
- When/where is it **transmitted** to another layer or service?
- When/where is it **persisted** (and is persistence actually guaranteed, or only conditional)?
- When/where is it **consumed/used** by another party?
- When/where is it **recovered or re-derived** (e.g. after logout/login, reconnect, retry)?

The root cause is very often a **gap between two of these stages** — something created in stage 1 that was never wired into stage 3, for example — rather than a bug within any single stage. Write the lifecycle out explicitly (even as a short list) before touching code; do not hold it only in your head.

### Technique 2: Extract precise user behavior as diagnostic data

When a person reports a bug, do not treat their description of *what they clicked and in what order* as incidental color — treat it as primary diagnostic evidence, often more valuable than the code itself for this class of bug.

- Ask for (or verify) the **exact sequence**: who did what, in what order, and what was each party's state at the time (online/offline, logged in/out, which tab/device).
- Actively translate each detail into a hypothesis: *"Why would that specific ordering matter? What state does it imply?"*
- A detail that seems like unrelated UX trivia (e.g. "the second user logged in after the first") is frequently the exact trigger condition for a timing-dependent bug.

### Technique 3: Bounded Context violation check

A very common root cause of systemic bugs: **data belonging to one domain gets implicitly tied to the state of a different, unrelated domain.**

- Actively look for any query, join, or cleanup logic that couples two conceptually separate domains — e.g. authentication/session state used as a condition for deleting or filtering data that belongs to a different domain (encryption keys, messages, profile data, etc.).
- Ask: *"Does domain A's data have any real business reason to depend on domain B's current state?"* If not, that coupling is the smell to investigate first.
- The fix for this class of bug is almost always to **decouple the two domains**, not to patch the specific query.

### Technique 4: Audit wide-scope mutations and background jobs

Bugs in this class often don't live in the main request/response flow at all — they live in a job running elsewhere that has a side effect on data the main flow depends on.

- Any `DELETE`, bulk `UPDATE`, or cleanup/garbage-collection job that runs on a schedule or on some unrelated trigger is a prime suspect — audit exactly what condition it filters on, and whether that condition can unintentionally match data it shouldn't touch.
- Ask specifically: *"What triggers this job to run, and could that trigger have just fired because of something unrelated to the bug report?"*

## Silent failures — handle with discipline, not by avoiding them

Swallowing an error silently (e.g. an empty `catch {}`) removes your best debugging signal and should not be done casually. If a codebase intentionally uses silent failure as a design choice (e.g. to keep a UI console clean, or because retry logic makes the failure non-fatal), that decision comes with an obligation:

- The layer that would have thrown must be made robust enough that the silent path is rarely taken (e.g. prefer reusing an already-derived value over regenerating one that can fail).
- Never let a silent failure hide a case that causes **permanent data loss** — if there's any chance the swallowed error represents unrecoverable state, it must be logged at minimum, even if it doesn't surface to the end user.

## After resolving a Phase 2 bug — write a short root cause note

Once fixed, write a brief note (in the PR description, commit message, or a project doc) covering:
- The lifecycle gap or domain-boundary violation that actually caused it (not just the symptom).
- Why it wasn't caught earlier — what assumption was wrong.
- Any other place in the codebase with the same pattern that should be checked (a wide-scope DELETE/UPDATE with the same smell rarely exists in only one place).

This note is what turns a one-off fix into prevention for the next bug of the same shape.

## Common anti-patterns to avoid

| # | Anti-pattern | Do instead |
|---|---|---|
| 1 | Re-reading the same files repeatedly across a debugging session without new information | Only re-read a file after something in it actually changed |
| 2 | Applying Fast Path narrowing to a bug that doesn't reproduce consistently | Escalate to Phase 2 after 2 failed Fast Path attempts |
| 3 | Fixing the symptom at the exact point it surfaced, without tracing back to where the data first went wrong | Trace the entity's full lifecycle before writing a fix |
| 4 | Treating the user's description of their exact steps as unnecessary detail | Treat exact sequence-of-actions as primary diagnostic data |
| 5 | Leaving a `catch {}` with no logging "because it's rare" | Log at minimum; never silently swallow a path that can cause permanent data loss |
| 6 | Fixing one instance of a wide-scope DELETE/UPDATE bug without checking for the same pattern elsewhere | Search the codebase for the same query/job pattern after fixing one instance |
| 7 | Closing the bug without writing down the actual root cause | Write a short root-cause note so the same class of bug is easier to catch next time |
