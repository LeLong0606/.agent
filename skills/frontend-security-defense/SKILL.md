# Frontend Security Defense (React/Vue/JS/TS)

> A checklist + code pattern reference to apply whenever you write or review frontend code that handles user-entered data or data from an API. Covers client-side aspects of 7 common attack vectors: XSS (DOM-based/reflected), CSRF (sending tokens correctly), CORS (calling cross-origin APIs safely), Rate Limiting (handling 429/backoff), Injection (avoiding rendering/evaluating uncontrolled data), and Security Headers (CSP via meta tag when you don't control the server).

---

## Workflow when writing frontend code

1. Does it render user-entered data or data from an API back into the page? → check for XSS risk
2. Does it call a write API (POST/PUT/DELETE) in an app using cookie-based auth? → needs a CSRF token
3. Does it call a cross-origin API? → understand CORS correctly, don't "fix" errors by disabling credentials incorrectly
4. Does it handle being rate-limited (429)? → needs sensible retry/backoff, not an infinitely locked UI
5. Where are sensitive tokens stored? → avoid `localStorage` for sensitive tokens if an HttpOnly cookie is possible
6. Does it use `innerHTML`, `dangerouslySetInnerHTML`, `v-html`, `eval`, or `new Function()`? → flag it and propose a safer alternative

---

## 1. XSS (the main frontend concern)

**Rule**: never inject uncontrolled data into the DOM as raw HTML.

```jsx
// ✅ SAFE - React auto-escapes when rendering via {}
<div>{userComment}</div>

// ❌ DANGEROUS - bypasses React's escaping
<div dangerouslySetInnerHTML={{ __html: userComment }} />

// If raw HTML is unavoidable (rich text from a CMS/editor) → sanitize first with DOMPurify
import DOMPurify from 'dompurify';
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(rawHtml) }} />
```

```vue
<!-- ❌ DANGEROUS -->
<div v-html="userComment"></div>

<!-- ✅ SAFE -->
<div>{{ userComment }}</div>
<!-- If raw HTML is required: -->
<div v-html="$sanitize(rawHtml)"></div> <!-- use DOMPurify the same way -->
```

```javascript
// DOM-based XSS - vanilla JS
// ❌ DANGEROUS
document.getElementById('output').innerHTML = userInput;

// ✅ SAFE
document.getElementById('output').textContent = userInput;

// ❌ EXTREMELY DANGEROUS - never eval data from a user or a URL
eval(userInput);
new Function(userInput)();

// URL/query string is also untrusted input
const q = new URLSearchParams(location.search).get('name');
document.title = q; // safe (not an HTML context)
element.innerHTML = q; // ❌ dangerous if q contains <script>
```

**When building dynamic URLs** (avoid `javascript:` URI injection):
```javascript
// ❌ DANGEROUS
link.href = userProvidedUrl; // could be "javascript:alert(1)"

// ✅ SAFE - whitelist the scheme
const url = new URL(userProvidedUrl, location.origin);
if (!['http:', 'https:'].includes(url.protocol)) throw new Error('Invalid URL');
link.href = url.toString();
```

---

## 2. CSRF (frontend side)

Only relevant when the backend uses cookie-based sessions. Standard flow:

```javascript
// 1. Fetch a CSRF token from the server (dedicated endpoint or double-submit cookie)
const { token } = await fetch('/api/csrf-token', { credentials: 'include' })
    .then(r => r.json());

// 2. Attach the token to every POST/PUT/DELETE request
await fetch('/api/transfer', {
    method: 'POST',
    credentials: 'include',
    headers: {
        'X-CSRF-TOKEN': token,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ amount: 100 })
});
```

With axios, use an interceptor to attach the token automatically instead of repeating it manually:

```javascript
axios.interceptors.request.use(config => {
    if (['post', 'put', 'delete', 'patch'].includes(config.method)) {
        config.headers['X-CSRF-TOKEN'] = getCsrfTokenFromMemoryOrCookie();
    }
    return config;
});
```

If the backend uses Bearer tokens (Authorization header) instead of cookies, CSRF is not a major concern and this step can be skipped.

---

## 3. CORS (frontend side)

The frontend doesn't "configure" CORS (that's the backend's job), but you need to understand it correctly to avoid creating a vulnerability:

```javascript
// credentials: 'include' only works if the backend has already whitelisted the correct origin
// DO NOT try to "fix" a CORS error by adding Access-Control-* headers on the client — that's meaningless, it must be fixed server-side
fetch('https://api.yourdomain.com/data', {
    credentials: 'include' // sends cookies cross-origin, requires backend AllowCredentials + a specific origin
});
```

- If you see a CORS error in the console, don't suggest the user disable CORS in the browser or install a bypass extension — that's a sign security is working correctly; the backend configuration needs to be fixed.
- Don't send sensitive tokens/API keys to an untrusted domain even if CORS technically allows it.

---

## 4. Rate Limiting (client-side handling)

```javascript
async function fetchWithRetry(url, options, maxRetries = 3) {
    for (let attempt = 0; attempt <= maxRetries; attempt++) {
        const res = await fetch(url, options);
        if (res.status !== 429) return res;

        const retryAfter = parseInt(res.headers.get('Retry-After') || '2', 10);
        const backoff = retryAfter * 1000 * Math.pow(2, attempt); // exponential backoff
        await new Promise(r => setTimeout(r, backoff));
    }
    throw new Error('Max retries exceeded');
}
```

- Debounce/throttle actions that fire API calls repeatedly (search-as-you-type, autosave) to avoid accidentally triggering rate limits and to reduce server load.
- Disable the submit button immediately on click to prevent double submits (good UX, and reduces the chance of looking like spam).

---

## 5. Injection (frontend perspective)

Injection is mostly a backend concern, but the frontend still plays a defensive role:
- Validate input on the client for better UX, but **never treat this as a real security layer** — always re-validate on the server.
- Don't build raw SQL-like query strings on the client and send them for the backend to execute directly. If an "advanced search" feature allows raw filter input, the backend must parse it safely, not execute it directly.
- Watch out for client-side libraries that render dynamic string templates (e.g. some chart/table libraries support "formulas") — these can lead to CSV/Excel injection when exporting files.

---

## 6. Token Storage & Client-Side Security Headers

```javascript
// Sensitive tokens (refresh token, session):
// ✅ Prefer HttpOnly cookies (JS can't read them, protecting against XSS-based theft)
// ⚠️ If localStorage/sessionStorage is unavoidable (e.g. short-lived access token for an SPA):
//    accept the higher XSS exposure risk, and compensate with a strict CSP and thorough input sanitization
```

If you don't control the server's response headers, a CSP can still be set via a meta tag (weaker than an HTTP header, but still useful):

```html
<meta http-equiv="Content-Security-Policy"
      content="default-src 'self'; script-src 'self'; object-src 'none';">
```

---

## Reviewing existing frontend code

Scan in order of severity: `dangerouslySetInnerHTML`/`v-html`/`innerHTML`/`eval` (XSS) → where tokens are stored → write requests missing a CSRF token → missing 429 handling → CSP.

## Scope / limitations

This guide focuses on **client-side defense**. Firewall/WAF is an infrastructure concern outside the scope of frontend work — when asked, briefly note that this is the backend/infra team's responsibility and point to the companion `backend-security-defense` guide if available.
