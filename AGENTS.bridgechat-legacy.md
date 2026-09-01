# Rule Set

## Automatic Workflow Routing

### Localization Ownership Boundary

* Frontend React UI translations belong exclusively to `bridgechatwebreact/public/locales/**`, using the existing frontend locale folders, namespaces, and translation hooks.
* Backend API, validation, and logging resources belong exclusively to `BridgeChat.SharedLibraries/Core.Localization/Resources/en-US.json`, `vi-VN.json`, and `zh-CN.json`.
* Never add frontend UI keys to `Core.Localization`. Never use backend `LocalizationKeys` from React.
* `Core.Localization/Generated/LocalizationKeys.g.cs` is generated backend hover metadata. Fix its JSON/template source and regenerate it; never patch the generated file directly.

Khi yêu cầu của người dùng khớp một trong các mẫu sau, agent phải tự động đọc và thực thi workflow tương ứng từ đầu đến cuối; người dùng không cần nhập slash command:

Before routing any BridgeChat request, the agent must execute `.agents/workflows/bridgechat-request-intake.md` to normalize the goal, infer probable service and UI scope, classify risk, choose the workflow chain, and automatically select relevant skills. The user does not need to name skills. Announce the selected chain briefly, then continue without an unnecessary approval pause.

* `Tiến hành đi vào trong <Tên dự án> và xây dựng tính năng <Tên tính năng>` hoặc câu tương đương về xây dựng tính năng backend/full-stack: dùng `.agents/workflows/bridgechat-build-feature.md`.
* `Tiến hành xây dựng giao diện cho tính năng <Tên tính năng>` hoặc câu tương đương về tích hợp frontend: dùng `.agents/workflows/bridgechat-build-ui.md`.
* `Tiến hành truy vết và sửa lỗi <Mô tả lỗi>`, status `4xx/5xx`, stack trace hoặc logs lỗi: dùng `.agents/workflows/bridgechat-fix-error.md`.

Mỗi workflow mẹ trước tiên phải thực thi `.agents/workflows/bridgechat-brain-context.md`: tìm walkthrough liên quan gần nhất trong cả ba Antigravity brain theo project/feature, tóm tắt phần đã làm, phần đang dở và quyết định phải giữ, rồi đối chiếu code hiện tại. Sau đó đọc `.agents/workflows/bridgechat-skill-router.md`, chọn đúng skill và tiếp tục qua điều tra, tổng hợp, triển khai, kiểm chứng, quality gate và bàn giao. Khi tính năng hoặc lỗi chạm từ hai service trở lên, integration event, shared contract, API Gateway, realtime hoặc frontend, phải áp dụng thêm `.agents/workflows/bridgechat-microservice-orchestration.md` để quản lý ownership, contract, consistency, recovery, distributed tests và rollout. Không dừng giữa các pha để chờ lệnh lặp lại, trừ khi cần quyết định nghiệp vụ không thể suy ra an toàn, quyền cho thao tác phá hủy/production, hoặc người dùng yêu cầu duyệt plan trước khi code.

Trước khi báo hoàn thành bất kỳ thay đổi nào, agent phải thực thi `.agents/workflows/bridgechat-text-integrity.md`. Việc file decode UTF-8 thành công chưa đủ: phải phát hiện và phục hồi cả mojibake/lossy tiếng Việt như `MA tAi`, `Ting Vit`, `MTt tin nhn`, xác nhận UTF-8 không BOM, CRLF, rồi chạy audit đến khi hai vòng liên tiếp không tạo thêm diff. Với generated localization code, phải sửa source JSON/template và regenerate thay vì vá tay file `.g.cs`.

### Rule 1: Data Access Architecture (Dapper & Infrastructure Encapsulation)

* It is **strictly forbidden** to use `Microsoft.EntityFrameworkCore` for data access or query execution in any form across the entire application (including Repositories). All data access must be implemented using **Dapper** with raw SQL queries to ensure maximum performance and minimize hardware resource consumption.
* It is **strictly forbidden** to execute direct SQL queries or use Dapper directly from the Application layer (including `IdentityService` or any similar service). All database logic must be fully encapsulated within the **Infrastructure** layer and exposed exclusively through **Repositories**.

---

### Rule 2: API Design, OpenAPI & Postman Automation (via MCP)

All HTTP APIs **must** follow RESTful principles regarding request transmission, HTTP semantics, and strict documentation standards.

#### HTTP Methods & Request Payload
* **HTTP GET** is **strictly prohibited** for any operation that requires input data or performs business processing. Operations requiring input data **must** use `POST`, `PUT`, or `PATCH` as appropriate.
* Client input data must **never** be passed through the URL, including Query string parameters, Route parameters, and Path variables.
* All request payloads must be transmitted exclusively in the **request body**.

#### Semantic HTTP Status Codes
HTTP responses **must** use the appropriate status codes according to their semantic meaning. Returning `200 OK` for every response regardless of the actual outcome is **strictly prohibited**.
Examples include:
* **200 OK** / **201 Created** / **202 Accepted** / **204 No Content**
* **400 Bad Request** / **401 Unauthorized** / **403 Forbidden** / **404 Not Found** / **409 Conflict** / **422 Unprocessable Entity** / **429 Too Many Requests**
* **500 Internal Server Error** / **502 Bad Gateway** / **503 Service Unavailable** / **504 Gateway Timeout**

#### OpenAPI & Metadata Configuration (C#)
* **Program.cs Configuration**: Update `builder.Services.AddOpenApi(...)` (or Swagger configuration) to support reading XML Documentation (generated from `/// <summary>` comments).
* **Strict Metadata Definition**: Scan all Controllers within the `Features` folder (following Vertical Slice Architecture). Ensure all APIs have comprehensive metadata attributes:
  * `[Produces("application/json")]`
  * `[ProducesResponseType(typeof(ApiResponse<T>), StatusCodes.Status...)]` for **ALL** potential HTTP status codes that the API can return.

#### Enterprise Postman Collection Automation (via MCP)
Use the MCP Postman tool to create or update API Collections (e.g., `BridgeChat IdentityService`) configured to automation standards:
* **VSA Directory Mapping**: The folder structure in Postman must map 1-to-1 with the `Features` directory structure in the source code (e.g., Auth, Roles, Sessions, E2EE).
* **Environment Variables**: Replace all hardcoded URLs with the `{{baseUrl}}` variable. Pre-create dynamic variables such as `{{accessToken}}` and `{{targetUserId}}`.
* **Automated Auth Flow (Hybrid Auth)**:
  * **Root Collection Level**: Configure Authorization as `Bearer Token` using the `{{accessToken}}` variable.
  * **Login & Refresh Token APIs**: Write Post-response scripts in the `Tests` tab to parse the JSON response, extract `data.accessToken`, and dynamically assign it to the environment variable: `pm.environment.set("accessToken", ...);`.
* **Auto-Generated Test Scripts (Auto-Assert)**:
  * Automatically generate Test scripts in the `Tests` tab for **ALL** APIs based on their expected default Status Codes.
  * Assert the Status Code (e.g., `pm.response.to.have.status(201);`).
  * Assert the JSON response structure (e.g., `pm.expect(jsonData.isSuccess).to.eql(true);`).
  * Assert Performance SLA: Ensure the response time is strictly `< 200ms` (e.g., `pm.expect(pm.response.responseTime).to.be.below(200);`).

*When explicitly asked to perform API configuration for Postman, the AI Agent must first display the necessary C# code changes, then execute the Postman Collection creation via MCP, and finally report the results.*

---

### Rule 3: Application Layer & Feature Structure (CQRS & VSA)

#### Request & Response
* Request (`Command`/`Query`) and `Response` records must be placed in separate files.
* All Response types must be declared as `record`, not `class`.
* Do not use the `Dto` suffix for Response records.
* If a feature only returns a status (such as `bool`) or a simple success message, do not create a redundant Response record.

#### Validation
* Every `Command` and `Query` **must** have a corresponding FluentValidation validator.
* Validators must use `IStringLocalizer<GlobalResource>` to retrieve validation messages from the centralized localization resources.
* If a validation key does not exist, it must be added to **en-US.json**, **vi-VN.json**, and **zh-CN.json**.

#### API Request Models
* Any API-specific request model used to receive `[FromBody]` data must be declared as a `public class`, **not** a `record`.
* Request models must **not** be nested inside a Controller.
* Request models must **not** be declared at the bottom of the Controller file.
* They must be placed in the corresponding Application Feature folder (e.g. `Application/Features/{FeatureName}/{FeatureName}Request.cs`).
* Do not use the `Dto` suffix.

#### Immutability Boundary
Data entering the Controller from the client must first be bound to a mutable `class` request model. After sanitization, validation, and enrichment with internal context (such as `UserId` from claims), it must be mapped into an immutable MediatR `Command` or `Query` record before entering the Application layer. The `record` represents a finalized, immutable message.

---

### Rule 4: Clean Code & Documentation Standards

#### File Encoding & Line Endings (CRLF & UTF-8)
It is **strictly mandatory** to maintain consistent file formatting across the entire repository to prevent cross-platform compilation issues and localization corruption:
* **Encoding**: Every file generated, modified, or saved must strictly use **UTF-8** encoding (`Select Encoding = UTF-8`). Generating files with alternative encodings (such as Windows-1252) is strictly prohibited.
* **End of Line (EOL)**: Every file must strictly use **CRLF** (Carriage Return Line Feed) for the end-of-line sequence (`Select end of line sequence = CRLF`).

#### Code Documentation & Comments (IdentityService Standard)
It is **mandatory** to provide **extremely detailed, comprehensive, and thorough documentation** throughout the codebase, taking `BridgeChat.IdentityService` as the gold standard. Documentation should be sufficiently detailed so that another developer can fully understand the design decisions, business rules, execution flow, and implementation.
* **Language**: All documentation (both `///` and `//`) must be written entirely in **Vietnamese**.
* **XML Documentation (`///`)**:
  - Must be applied to **all** classes, constructors, methods, properties, enums, interfaces, and public members.
  - **Controllers & Endpoints**: Must heavily use `<summary>` for the main purpose and `<remarks>` for deep technical/architectural context (e.g., security strategies, CQRS delegation, XSS/CSRF mitigations). Use `<list type="bullet">` and `<item>` inside `<remarks>` for structured formatting.
  - **Records**: For C# `record` types, `<param name="...">` **must** be placed above the `public record` declaration (not inside the constructor parameters) to prevent `CS1587` compiler errors.
* **Inline Comments (`//`)**:
  - Must use numbered steps (`// 1.`, `// 2.`, etc.) inside complex methods (especially CQRS handlers and Controllers) to outline the chronological business flow step-by-step.
  - Must clearly explain both **why** the logic exists (design decisions, business rules, Saga triggers) and **how** it works. Complex logic must **never** be left undocumented or explained with vague comments.
  - **Natural Language Requirement**: Write explanations naturally and fluently in normal sentences. It is **strictly forbidden** to explicitly write out metadata tags like `Giải thích (Why):` or `Cụ thể (How):`. The rule is meant to enforce deep context, not mechanical templating.

#### Fully Qualified Name Restriction
It is **strictly forbidden** to use fully qualified names (full namespace references) to access any class, method, property, or other type inside a method body if the corresponding namespace has already been imported with a `using` directive.
* **Exception**: The only exception is when a naming conflict exists (for example, multiple imported namespaces contain a class with the same name). In such cases, **using aliases** must be used as the preferred solution instead of writing fully qualified names inside the method body. Direct use of fully qualified names inside method bodies is permitted **only when aliasing is genuinely impractical or impossible**.

---

### Rule 5: System Logging, Exception Messages & Localization

#### 1. Hardcoded Strings Prohibition
It is **strictly forbidden** to hardcode string literals for any system messages or user-facing messages, including but not limited to:
- Exception messages thrown in the Application Layer (e.g., `throw new BadRequestException("...");`)
- System logs written via `_logger` (`ILogger<T>`)
- Validation messages (as defined in Rule 3)

#### 2. Centralized Localization Resources
All messages **must** be localized using `IStringLocalizer<GlobalResource>`. 
If a required message key does not exist, it **must** be added to **ALL THREE** centralized JSON resource files before being used in the code:
- `BridgeChat.SharedLibraries\Core.Localization\Resources\en-US.json`
- `BridgeChat.SharedLibraries\Core.Localization\Resources\vi-VN.json`
- `BridgeChat.SharedLibraries\Core.Localization\Resources\zh-CN.json`

#### 3. Thread Culture & Request Localization

To ensure that backend system logs remain readable and consistent in a specific language (e.g., `vi-VN` for the development team), while still preserving dynamic multi-language support for user-facing API responses, the following architectural standard must be applied:

* The default thread culture **must** be explicitly defined at the very beginning of the `Program.cs` file across all microservices. This guarantees that background workers (e.g., MassTransit Consumers, Quartz Jobs) which lack an `HttpContext` will default to the defined culture.

**Mandatory Implementation in `Program.cs`:**
```csharp
using System.Globalization;

CultureInfo.DefaultThreadCurrentCulture = new CultureInfo("vi-VN");
CultureInfo.DefaultThreadCurrentUICulture = new CultureInfo("vi-VN");

var builder = WebApplication.CreateBuilder(args);
// ...
```

* User-facing HTTP API responses will automatically override this default culture on a per-request basis via the `UseRequestLocalization()` middleware, ensuring the end-user receives the appropriate language without affecting the language used in developer system logs.

#### API Gateway Compatibility & Routing Standard
* It is **strictly forbidden** to use [Route("api/[controller]")] or any route that depends on the [controller] macro. This leads to wildcard configuration issues in the API Gateway and non-standard RESTful URL casing.
* All controllers **must** define a specific, explicit static route using the pattern [Route("api/{service-prefix}/{resource}")] where {service-prefix} is the unique identifier for the microservice (e.g., identity, users, chat, ttachments) and {resource} is a plural, lowercase kebab-case noun (e.g., uth, profiles, conversations).
* This ensures that API Gateway (YARP/Ocelot) can easily route traffic using wildcards like /api/identity/{**catch-all}.
