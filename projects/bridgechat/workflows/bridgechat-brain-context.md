---
name: bridgechat-brain-context
description: Restore relevant BridgeChat context from Antigravity brain walkthroughs before implementation, UI, or debugging work.
version: 3.0.0
requires_skills: antigravity-walkthrough-handoff
artifact_outputs: prior-work-summary, decisions, completed-work, pending-work, known-risks
---

# /bridgechat-brain-context — Cross-conversation bootstrap

$ARGUMENTS

Run this as Phase 0 of every parent workflow.

1. Extract project/service, feature/domain, endpoint/event/error key, and frontend/backend scope.
2. Search all existing roots: %USERPROFILE%\.gemini\antigravity-ide\brain\, %USERPROFILE%\.gemini\antigravity\brain\, and %USERPROFILE%\.gemini\antigravity-cli\brain\.
3. Sort conversations by newest modification time, then filter walkthrough*.md by project/topic before opening files. Reject unrelated topics.
4. Rank project + feature matches above project-only or feature-only matches. If equally strong candidates conflict, ask the user instead of guessing.
5. Read the selected walkthrough completely. Read task.md only when completion is unclear, implementation_plan.md only for original scope/reasoning, and JSONL only as a last resort.
6. Before code, summarize selected conversation, completed work, pending/deferred work, decisions, and known issues in 2–4 lines.
7. Verify history against current code and Git status. Code is current-state evidence; walkthrough preserves intent.
8. If no relevant walkthrough exists, state that and continue from source, tests, Git state, and runtime evidence.

Return: brain source/conversation, matched topic, completed, pending, decisions, known issues, mentioned files/services, and confidence.
