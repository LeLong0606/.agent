# BridgeChat Project Profile

This profile contains mandatory BridgeChat-specific rules. It extends `.agents/core/engineering-rules.md` and the shared skill selection policy in `.agents/core/skill-routing.md`.

## Workflow root

All BridgeChat-specific workflows live under `.agents/projects/bridgechat/workflows/`.

Before routing a BridgeChat request, execute `.agents/projects/bridgechat/workflows/bridgechat-request-intake.md`.

Then select the appropriate workflow:

- Backend/full-stack feature: `.agents/projects/bridgechat/workflows/bridgechat-build-feature.md`
- Frontend/UI feature: `.agents/projects/bridgechat/workflows/bridgechat-build-ui.md`
- Error/4xx/5xx/stack trace/log issue: `.agents/projects/bridgechat/workflows/bridgechat-fix-error.md`

Each parent workflow preserves the BridgeChat chain for brain context, skill routing, investigation, implementation, verification, handoff, text integrity, and microservice orchestration where applicable.

For BridgeChat frontend changes, additionally run `.agents/workflows/frontend-quality-gate.md` before final completion.

## Localization Ownership Boundary

- React UI translations belong exclusively to `bridgechatwebreact/public/locales/**` using existing locale folders, namespaces, and hooks.
- Backend API, validation, and logging resources belong exclusively to `BridgeChat.SharedLibraries/Core.Localization/Resources/en-US.json`, `vi-VN.json`, and `zh-CN.json`.
- Never add frontend UI keys to `Core.Localization` and never use backend `LocalizationKeys` from React.
- `Core.Localization/Generated/LocalizationKeys.g.cs` is generated. Fix source JSON/template and regenerate; never patch it directly.

## Data Access Architecture

- Entity Framework Core is forbidden for BridgeChat data access/query execution.
- Use Dapper with raw SQL through the Infrastructure layer.
- Application-layer services/handlers must not execute SQL or use Dapper directly.
- Database logic must be encapsulated by Infrastructure repositories.

## API Design

- Follow BridgeChat REST and API Gateway conventions.
- Do not use controller-name route macros such as `[Route("api/[controller]")]`.
- Use explicit static lowercase service/resource routes suitable for gateway wildcard routing.
- Preserve semantic HTTP status codes rather than returning `200 OK` for every outcome.
- Maintain OpenAPI response metadata for actual endpoint outcomes.
- Preserve existing BridgeChat request-body conventions unless the user explicitly changes the API contract.

## Application Layer / VSA / CQRS

- Command/Query and Response records belong in separate files.
- Response types are records and should not use a `Dto` suffix.
- Do not create redundant response records for trivial status-only results.
- Every Command/Query requires a FluentValidation validator.
- Validation messages use centralized localization resources.
- API body request models are mutable public classes in the corresponding Application Feature folder, not nested in controllers.
- Map sanitized/enriched request models into immutable MediatR Command/Query records before entering the Application layer.

## Encoding and Documentation

- Preserve UTF-8 and CRLF according to BridgeChat repository policy.
- Run `.agents/projects/bridgechat/workflows/bridgechat-text-integrity.md` before completion.
- Detect Vietnamese mojibake/lossy text; UTF-8 decode success alone is insufficient.
- Generated localization code must be regenerated from source rather than patched manually.
- Preserve existing BridgeChat Vietnamese documentation/comment conventions where required.

## Logging and Localization

- Do not hardcode user-facing/system message literals where BridgeChat localization is required.
- Use `IStringLocalizer<GlobalResource>` and keep all three centralized locale files synchronized when adding backend keys.
- Preserve BridgeChat request localization and default background-thread culture behavior.

## Legacy reference

`.agents/AGENTS.bridgechat-legacy.md` remains read-only migration reference. New rules must be added to this project profile, not the legacy file.
