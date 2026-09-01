---
name: bridgechat-debug
description: Diagnose and fix BridgeChat failures across layers using runtime evidence and regression tests.
version: 3.0.0
requires_workflows: bridgechat-request-intake, bridgechat-brain-context, bridgechat-fix-error, bridgechat-text-integrity
artifact_outputs: root-cause, fix, regression-tests, verification-report
---

# /bridgechat-debug

$ARGUMENTS

Reproduce the failure, capture request/status/body/correlation/time, inspect Gateway and downstream logs, and trace UI through storage/broker/cache/realtime. Prove the root cause before editing. Apply the smallest architectural fix, add regression coverage, verify runtime behavior, then run text-integrity and quality gates. Never reset data, delete volumes, or commit/push without explicit authorization.
