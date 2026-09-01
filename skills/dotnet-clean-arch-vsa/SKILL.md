---
name: dotnet-clean-arch-vsa
description: Guidance for creating new Features/Use Cases in a .NET project following a 4-layer Clean Architecture combined with Vertical Slice Architecture (VSA). Use this whenever creating a new Command/Query, adding a new endpoint, creating a new Feature, or scaffolding code for a microservice using the MediatR + FluentValidation + Dapper pattern. Covers standard folder structure, naming conventions, required technical patterns, and a checklist of common mistakes to avoid. ALWAYS use this skill before writing any Command, Query, Handler, Validator, Controller, or Repository code in a project following this architecture — even when the request only mentions "add an API", "add a feature", or "fix an endpoint". For detailed implementation code samples, see the accompanying `references/code-examples.md`.
---

# Clean Architecture + Vertical Slice Architecture (.NET)

Guidance for writing new code in a .NET project that follows a 4-layer Clean Architecture, where each Use Case (Feature) is organized as a Vertical Slice — all files related to one feature live together in one folder, instead of being spread across horizontal layers.

## When to use this skill

- Creating a new Command or Query (e.g. "add a change-password feature", "add an API to list orders")
- Adding a new endpoint to an existing Controller, or creating a new Controller
- Creating a new Repository or adding a method to an existing one
- Refactoring existing code to conform to this architecture's conventions
- Reviewing already-written code to check it follows the pattern correctly

## 1. Folder structure (4-Layer Clean Architecture)

Each microservice is its own solution, made up of 4 projects:

```
{ServiceName}/
├── {ServiceName}.Api/                    ← Presentation Layer
│   ├── Features/{FeatureArea}/           ← Contains ONLY Controllers (1 file per Feature Area)
│   ├── Program.cs                        ← DI composition root
│   └── Dockerfile
│
├── {ServiceName}.Application/            ← Application Layer (CQRS)
│   ├── Features/{FeatureArea}/{SliceName}/   ★ VERTICAL SLICE lives here ★
│   ├── Behaviors/ValidationBehavior.cs
│   ├── Interfaces/I{EntityGroup}Repository.cs
│   └── DependencyInjection.cs
│
├── {ServiceName}.Domain/                 ← Domain Layer
│   └── Entities/{EntityName}.cs          ← Plain entity, no business logic
│
└── {ServiceName}.Infrastructure/         ← Infrastructure Layer
    ├── Data/{ServiceName}DbContext.cs    ← ONLY used for Migrations, NEVER for queries
    └── Repositories/{EntityGroup}Repository.cs
```

**Important — the two-tier Features model:**

| Layer | What `Features/` contains | Granularity |
|---|---|---|
| **Api** | Controllers (1 file per Feature Area) | Grouped by Feature Area: `Authentication/`, `Sessions/`... |
| **Application** | Command/Query + Handler + Validator + Request + Response | Grouped by specific Use Case: `VerifyOtp/`, `GetActiveSessions/`... |

→ The actual Vertical Slice lives in the **Application layer**. There is no separate project dedicated to VSA.

## 2. What's inside each Slice

Each Slice (e.g. `VerifyOtp/`) has up to 5 files, **each component in its own separate file — never combined into one**:

| File | Role | C# type |
|---|---|---|
| `{Slice}Command.cs` or `{Slice}Query.cs` | MediatR message | `record` |
| `{Slice}CommandHandler.cs` / `{Slice}QueryHandler.cs` | Business logic | `class` |
| `{Slice}Validator.cs` | FluentValidation | `class` |
| `{Slice}Request.cs` | API request model (`[FromBody]`) — ONLY create when there's a client payload | `class` |
| `{Slice}Response.cs` | Response DTO | `record` |

**Rule for when to include a Request model:**
- **Include** a `Request` class when the Controller accepts a `[FromBody]` payload from the client.
- **Omit** it when the data comes from JWT Claims or a Cookie (no body payload).

All files within one slice share the same namespace: `...Features.{FeatureArea}.{SliceName}`.

## 3. Naming conventions

| Component | Pattern | Example |
|---|---|---|
| Command | `{Action}{Entity}Command` | `VerifyOtpCommand` |
| Query | `{Action}{Entity}Query` | `GetActiveSessionsQuery` |
| Command Handler | `{Action}{Entity}CommandHandler` | `VerifyOtpCommandHandler` |
| Query Handler | `{Action}{Entity}QueryHandler` | `GetActiveSessionsQueryHandler` |
| Validator | `{Action}{Entity}Validator` | `VerifyOtpValidator` |
| Request | `{Action}{Entity}Request` | `VerifyOtpRequest` |
| Response | `{Action}{Entity}Response` | `VerifyOtpResponse` |
| Controller | `{FeatureArea}Controller` | `SessionsController` |
| Repository | `{EntityGroup}Repository` | `SessionRepository` |
| Repository Interface | `I{EntityGroup}Repository` | `ISessionRepository` |

**Note:** MediatR messages always use the `Command`/`Query` suffix — never `Request` for a MediatR message name (this avoids confusion with the API Request model).

Namespaces follow the **folder structure**, not the layer:
```csharp
namespace {ServiceName}.Application.Features.{FeatureArea}.{SliceName};
namespace {ServiceName}.Api.Features.{FeatureArea};
namespace {ServiceName}.Domain.Entities;
namespace {ServiceName}.Infrastructure.Repositories;
```

## 4. Required technical patterns

| Category | Rule |
|---|---|
| **CQRS Dispatcher** | MediatR — Controllers inject `ISender` |
| **Validation** | FluentValidation, validates the Command/Query directly (NOT the Request class), runs through the `ValidationBehavior` pipeline |
| **Messages/errors** | Always sourced from `IStringLocalizer<GlobalResource>["KEY"]` — NEVER hardcoded strings |
| **API style** | Controller-based (NOT Minimal API) |
| **HTTP Method** | **All endpoints use POST**, including reads (no GET) |
| **Route** | `[Route("api/{service}/{resource}")]` — fixed, NEVER use the `[controller]` wildcard |
| **Response wrapper** | Always wrapped in `ApiResponse<T>`, returned via `StatusCode(result.StatusCode, result)` — NEVER `Ok(result)` |
| **Error handling** | Throw exceptions (`UnauthorizedException`, `BadRequestException`, `ValidationException`, `NotFoundException`) — do NOT use the `Result<T>` pattern |
| **Data access** | Dapper + raw SQL for all queries. EF Core is ONLY used for Migrations, NEVER for data queries |
| **Repository** | Interface declared in the Application layer, implementation in the Infrastructure layer |
| **SQL location** | All SQL/Dapper code lives inside a Repository (Infrastructure) — never write SQL in the Application layer |
| **Handler comments** | Number each step clearly (`// 1. Check OTP in Redis`, `// 2. ...`) |
| **Controller attributes** | Always include `[Produces("application/json")]` at class level and full `[ProducesResponseType]` for every possible status code |

## 5. Domain Layer

- The Domain layer currently follows an **Anemic Domain Model** — entities only hold properties, no business logic.
- Every Entity inherits from `BaseEntity` (provides `Id`, `CreatedAt`, `UpdatedAt`, `CreatedBy`, `UpdatedBy`).
- Use `init` for properties that are immutable after creation; use `set` only for properties that need runtime updates.
- **Do not** use Value Objects, Domain Events, or a separate `AggregateRoot` base class — if an event needs to be published, use an Integration Event via MassTransit instead of a Domain Event.

## 6. Reference code samples

See `references/code-examples.md` for complete code samples, including:
- A full Command Slice (VerifyOtp — 5 files: Command, Request, Response, Validator, Handler)
- A full Query Slice (GetActiveSessions — 4 files)
- A sample Controller and a sample Repository (Dapper)
- A sequence diagram describing the flow from Client → Controller → MediatR → Handler → Repository → DB

Only open this file when you need to see the exact implementation of a specific component (e.g. "not sure how the Validator should look" → check the Validator section in the reference file).

## 7. Common mistakes — ALWAYS check before considering the work done

| # | Mistake | Correct approach |
|---|---|---|
| 1 | Using EF Core LINQ to query data | Use Dapper + raw SQL inside the Repository |
| 2 | Combining Command + Handler + Validator into one file | Each component gets its own separate file |
| 3 | Using a `record` for the Request model | Request must be a `class` (mutable) |
| 4 | Nesting the Request model inside the Controller, or suffixing it with `Dto` | Separate file inside the Feature folder, no `Dto` suffix |
| 5 | Hardcoding strings for exception/validation messages | Always source from `_localizer["KEY"]` |
| 6 | Using `[Route("api/[controller]")]` | Use a fixed route: `[Route("api/{service}/{resource}")]` |
| 7 | Using HTTP GET for read endpoints | Always use POST |
| 8 | Forgetting to create a Validator for a Command/Query | Every Command/Query must have a Validator, even a simple one |
| 9 | Returning `Ok(result)` | Return `StatusCode(result.StatusCode, result)` |
| 10 | Writing SQL/Dapper code directly in the Application layer | All DB access is encapsulated in a Repository (Infrastructure) |
| 11 | Missing numbered step comments in a Handler | Always number the steps clearly (`// 1. ...`, `// 2. ...`) |
| 12 | Missing `[Produces]` / `[ProducesResponseType]` on the Controller | Always declare them fully |

## General principles when applying this skill

When asked to create a new Feature/Use Case, always:
1. Determine whether it's a Command (mutates data) or a Query (reads data).
2. Create all the files following the structure in section 2, named according to section 3.
3. Apply the required technical patterns from section 4 (Dapper, POST, ApiResponse wrapper, throwing exceptions, etc.).
4. Cross-check against the common mistakes table in section 7 before considering the task complete.
5. If anything is unclear about a service-specific convention (e.g. table names, DB field names), ask rather than guess.
