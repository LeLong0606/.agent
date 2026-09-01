---
name: postman-collection-automation
description: Guidance for creating or updating a Postman Collection via the Postman MCP tool for a .NET microservice built with Vertical Slice Architecture. Use this whenever explicitly asked to "set up Postman", "configure API for Postman", "update the Postman collection", or "automate Postman testing" for a service. Covers folder-to-Features mapping, environment variables, automated Bearer auth flow (login/refresh token scripts), and auto-generated test/assertion scripts. Do NOT use this for general API design questions unrelated to Postman — those belong in the `dotnet-clean-arch-vsa` skill instead.
---

# Postman Collection Automation (via MCP)

Guidance for creating or updating an Enterprise-grade Postman Collection through the Postman MCP tool, kept in sync with a .NET microservice's Vertical Slice Architecture.

## When to use this skill

- Explicitly asked to create or update a Postman Collection for a service (e.g. "set up Postman for BridgeChat IdentityService")
- Asked to add automated test scripts, environment variables, or auth flow to an existing Postman Collection
- Asked to keep a Postman Collection folder structure in sync with the codebase's `Features` folders

## Required workflow order

When explicitly asked to perform API configuration for Postman, always follow this exact order:
1. **First**, display the necessary C# code changes (OpenAPI/Swagger metadata updates — see section 1 below).
2. **Then**, execute the Postman Collection creation/update via the MCP Postman tool.
3. **Finally**, report the results back to the user.

Never skip step 1 — Postman documentation quality depends on the underlying OpenAPI metadata being correct first.

## 1. OpenAPI & metadata prerequisites (C# side)

Before touching Postman, make sure the API itself is properly documented:

- **`Program.cs`**: `builder.Services.AddOpenApi(...)` (or Swagger config) must be set up to read XML documentation generated from `/// <summary>` comments.
- **Controller scan scope**: scan all Controllers inside the `Features` folder (Vertical Slice Architecture) — not just a subset.
- Every endpoint must have:
  - `[Produces("application/json")]`
  - `[ProducesResponseType(typeof(ApiResponse<T>), StatusCodes.Status...)]` for **every** possible status code the endpoint can return.

## 2. Collection structure — 1-to-1 mapping with source code

The Postman folder structure must mirror the `Features` directory structure in the codebase exactly:

```
Postman Collection: {ServiceName}
├── Auth/           ← mirrors Features/Authentication/
├── Roles/          ← mirrors Features/Roles/
├── Sessions/        ← mirrors Features/Sessions/
└── E2EE/            ← mirrors Features/E2EE/
```

If a new Feature Area is added to the codebase, add a matching folder to the Collection — never flatten multiple Feature Areas into one folder.

## 3. Environment variables — never hardcode URLs

- Replace all hardcoded URLs with `{{baseUrl}}`.
- Pre-create dynamic variables used across requests, at minimum:
  - `{{accessToken}}`
  - `{{targetUserId}}`
- Add any other per-service dynamic variable needed by the flow (e.g. `{{refreshToken}}`, `{{sessionId}}`) rather than hardcoding sample values.

## 4. Automated auth flow (Hybrid Auth)

- **Root Collection level**: set Authorization type to `Bearer Token`, using `{{accessToken}}`.
- **Login & Refresh Token requests specifically**: add a Post-response script in the `Tests` tab that parses the JSON response, extracts `data.accessToken`, and assigns it back to the environment:

```javascript
const jsonData = pm.response.json();
pm.environment.set("accessToken", jsonData.data.accessToken);
```

This keeps every other request in the Collection automatically authenticated without manual token copy-pasting.

## 5. Auto-generated test scripts (Auto-Assert)

Generate a `Tests` tab script for **every** request in the Collection, covering at minimum:

- **Status code assertion**, matching the endpoint's expected default status:
  ```javascript
  pm.test("Status code is 201", function () {
      pm.response.to.have.status(201);
  });
  ```
- **Response shape assertion**:
  ```javascript
  pm.test("Response has isSuccess = true", function () {
      const jsonData = pm.response.json();
      pm.expect(jsonData.isSuccess).to.eql(true);
  });
  ```
- **Performance SLA assertion** — response time strictly under 200ms:
  ```javascript
  pm.test("Response time is below 200ms", function () {
      pm.expect(pm.response.responseTime).to.be.below(200);
  });
  ```

Do not skip the SLA assertion even for endpoints that "feel" fast — it must be present on every request so regressions are caught automatically.

## Common mistakes to avoid

| # | Mistake | Correct approach |
|---|---|---|
| 1 | Doing the Postman MCP work before showing the C# metadata changes | Always show code changes first, then execute Postman automation |
| 2 | Hardcoding a URL or token value directly in a request | Use `{{baseUrl}}`, `{{accessToken}}`, etc. |
| 3 | Flattening multiple Feature Areas into one Postman folder | Keep a strict 1-to-1 folder-to-Feature-Area mapping |
| 4 | Skipping the SLA assertion on "simple" endpoints | Add the `< 200ms` assertion to every request without exception |
| 5 | Setting Bearer auth per-request instead of at Collection root | Configure Bearer Token once at the root Collection level |
