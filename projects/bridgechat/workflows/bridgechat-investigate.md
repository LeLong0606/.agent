---
name: bridgechat-investigate
description: Investigate BridgeChat from evidence and report findings without modifying code.
version: 3.0.0
requires_workflows: bridgechat-request-intake, bridgechat-brain-context, bridgechat-skill-router
artifact_outputs: investigation-report, root-cause, evidence
---

# /bridgechat-investigate

$ARGUMENTS

Run brain context first. Identify service, endpoint, UI flow, container, and scope. Collect code, request/response, logs, and storage evidence. Trace React → Gateway → Controller → Application → Infrastructure → DB/cache/broker → consumer/realtime. Compare with AGENTS.md and relevant skills. Report symptom, root cause, evidence, impact, repair options, risks, and verification. Do not modify files, data, containers, or configuration.
