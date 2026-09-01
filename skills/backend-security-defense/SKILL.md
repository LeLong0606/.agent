# Backend Security Defense (ASP.NET Core / C#)

> A checklist + code pattern reference to apply whenever you write or review backend code that accepts external input (API, form, query string, header, file upload...). Covers 7 common attack vectors: Rate Limiting abuse, CORS misconfiguration, Injection, missing Firewall/network hardening, CSRF, XSS (server-side output encoding), and missing Security Headers/HTTPS.

---

## Workflow when writing a new endpoint/API

Before shipping code, ask (and apply) these in order:

1. Does this endpoint need rate limiting? (Almost always — especially login, OTP, password reset, search, upload, or any call to a paid external API)
2. Does it feed user input into a query/command/file path? → must be parameterized/validated
3. Which domain(s) is it called from? → configure CORS correctly, never `AllowAny` when cookies/credentials are involved
4. Does it use cookie-based auth? → needs a CSRF token + `SameSite` cookie
5. Does the output render user data back (HTML, JSON, email)? → encode correctly for the context
6. Are response headers already set with CSP/HSTS/nosniff?

Even if the user only asks about one piece (e.g. "write a login endpoint"), automatically apply all the relevant pieces (rate limit + CSRF/cookie + injection-safe query) without needing to be asked individually.

---

## 1. Rate Limiting

Use `Microsoft.AspNetCore.RateLimiting` (built-in since .NET 7+, stable on .NET 8/9/10). Defaults:
- Regular endpoints: fixed/sliding window, 100 req/min per IP (or per user ID if authenticated).
- Sensitive endpoints (login, OTP, forgot-password, register): sliding window, 5 req/5 min per IP + per target account.
- Resource-heavy endpoints (export, upload, calls to external/AI APIs): concurrency limiter.

```csharp
builder.Services.AddRateLimiter(options =>
{
    options.AddPolicy("login", httpContext =>
        RateLimitPartition.GetSlidingWindowLimiter(
            httpContext.Connection.RemoteIpAddress?.ToString() ?? "unknown",
            _ => new SlidingWindowRateLimiterOptions
            {
                PermitLimit = 5, Window = TimeSpan.FromMinutes(5),
                SegmentsPerWindow = 5, QueueLimit = 0
            }));
    options.RejectionStatusCode = StatusCodes.Status429TooManyRequests;
});
app.UseRateLimiter();
app.MapPost("/api/login", LoginHandler).RequireRateLimiting("login");
```

Note: behind a reverse proxy (Nginx/Cloudflare), configure `ForwardedHeaders` to get the real client IP, trusting only internal proxies.

---

## 2. CORS

- Cookie-based auth → whitelist specific origins with `WithOrigins(...)`, NEVER combine `AllowAnyOrigin()` with `AllowCredentials()`.
- Bearer token in header → lower risk, but still whitelist origins unless the API is genuinely public.
- Always restrict `WithMethods` and `WithHeaders`, avoid "Any".

```csharp
builder.Services.AddCors(o => o.AddPolicy("AppPolicy", p => p
    .WithOrigins("https://app.yourdomain.com")
    .WithMethods("GET", "POST", "PUT", "DELETE")
    .WithHeaders("Content-Type", "Authorization")
    .AllowCredentials()));
app.UseCors("AppPolicy"); // after UseRouting, before UseAuthorization
```

---

## 3. Injection

Hard rule: **never concatenate user input directly into SQL/command/path/XML**.

- SQL: use EF Core LINQ or `FromSqlInterpolated`, or `SqlCommand` with `Parameters.AddWithValue`. Never use `FromSqlRaw($"...")` with direct string interpolation.
- Command: use `ProcessStartInfo.ArgumentList` (not a hand-built `Arguments` string), validate input with a strict whitelist/regex before use.
- Path traversal: use `Path.GetFileName()` to strip path segments, then verify `fullPath.StartsWith(basePath)` after `Path.GetFullPath`.
- XML: set `DtdProcessing = DtdProcessing.Prohibit` and `XmlResolver = null` when parsing XML from external input.
- App DB user: least privilege — never `sa`/`root`.

```csharp
// Safe SQL
var user = await db.Users.FirstOrDefaultAsync(u => u.Username == username);

// Safe command execution
var psi = new ProcessStartInfo {
    FileName = "ping", ArgumentList = { "-n", "4", validatedIp }, UseShellExecute = false
};
```

---

## 4. Firewall / Network Hardening

Mostly infrastructure configuration, not code — but flag this during review/deploy:
- Only expose 443 (and 80 redirecting to it) to the internet; close DB ports (1433/5432/27017), RDP (3389), SSH (22) from public access — VPN/bastion only.
- Enable a WAF at the CDN/Load Balancer layer if available (Cloudflare, Azure Front Door, AWS WAF).
- Database should only accept connections from the app server's subnet.
- An in-code IP-blocking middleware (`app.Use(async (ctx, next) => {...})`) is only a supplementary layer — it does NOT replace a real firewall. Say this explicitly if the user is relying solely on code for this.

---

## 5. CSRF

Only a serious concern with **cookie-based authentication**. If using pure Bearer tokens in headers, CSRF risk is nearly nonexistent (still worth setting `SameSite` as a safety net).

```csharp
builder.Services.AddAntiforgery(o => {
    o.HeaderName = "X-CSRF-TOKEN";
    o.Cookie.SecurePolicy = CookieSecurePolicy.Always;
    o.Cookie.SameSite = SameSiteMode.Strict;
});
app.UseAntiforgery();

builder.Services.ConfigureApplicationCookie(o => {
    o.Cookie.SameSite = SameSiteMode.Strict;
    o.Cookie.SecurePolicy = CookieSecurePolicy.Always;
    o.Cookie.HttpOnly = true;
});
```

MVC/Razor: use `[ValidateAntiForgeryToken]` on POST actions + `@Html.AntiForgeryToken()` in forms.
Minimal API/SPA: expose a `/api/csrf-token` endpoint returning a token; the frontend sends it back via the `X-CSRF-TOKEN` header.

---

## 6. XSS (server side)

- Razor auto-HTML-encodes `@variable` — don't use `Html.Raw()` with unsanitized input.
- If rich text must be allowed: use the `HtmlSanitizer` library (NuGet `Ganss.Xss`), with an explicit tag/attribute whitelist — never hand-roll a regex tag filter.
- JSON returned to a SPA: `System.Text.Json` escapes safely for HTML context by default.
- Session cookies should always be `HttpOnly` so JS can't read them even if XSS slips through.

```csharp
var sanitizer = new HtmlSanitizer();
sanitizer.AllowedTags.Clear();
sanitizer.AllowedTags.UnionWith(new[] { "b", "i", "p" });
sanitizer.AllowedAttributes.Clear();
var safeHtml = sanitizer.Sanitize(userInputHtml);
```

---

## 7. Security Headers & HTTPS

Add middleware to set headers on every response, and enforce HTTPS:

```csharp
app.Use(async (ctx, next) => {
    ctx.Response.Headers["X-Content-Type-Options"] = "nosniff";
    ctx.Response.Headers["X-Frame-Options"] = "DENY";
    ctx.Response.Headers["Referrer-Policy"] = "strict-origin-when-cross-origin";
    ctx.Response.Headers["Content-Security-Policy"] =
        "default-src 'self'; script-src 'self'; object-src 'none'; frame-ancestors 'none';";
    await next();
});
app.UseHsts();
app.UseHttpsRedirection();
```

---

## Reviewing existing code

Scan through all 7 areas above and report as: **[Area] → Issue found → Suggested fix (code)**. Prioritize Injection and CSRF/cookie issues first (highest severity), then Rate Limiting/CORS/Headers.

## Scope / limitations

This guide focuses on **application-layer defense** in C# code. For real Firewall/WAF protection (network layer), it only offers infrastructure recommendations — it can't configure Azure/AWS/Cloudflare for you without more specific infrastructure context.
