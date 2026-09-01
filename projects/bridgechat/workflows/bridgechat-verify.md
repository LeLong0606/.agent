---
name: bridgechat-verify
description: Verify BridgeChat changes through diff review, build, tests, localization ownership, runtime behavior, and encoding audits.
version: 3.0.0
requires_workflows: bridgechat-request-intake, bridgechat-text-integrity
artifact_outputs: verification-report, defect-list
---

# /bridgechat-verify

$ARGUMENTS

Identify exact changed files. Review architecture, authorization, validation, status semantics, transaction/concurrency, and hardcoded strings. Verify frontend locale changes only under bridgechatwebreact/public/locales/** and backend locale changes only under Core.Localization resources. Run relevant typecheck/lint/tests/build and runtime flow. Run text-integrity and all applicable architecture/localization audits until stable. Report PASS/FAIL with command evidence; never use “looks fine” as proof and never commit/push/deploy.
