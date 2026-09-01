# Portable Frontend Checklist

Use this bundled reference for deep or offline audits. Load only the categories relevant to the changed routes and components. Every finding still needs direct code, DOM, rendered-page, network, or test evidence.

## HTML and document structure

- Use one document language and valid charset/viewport declarations at the document owner.
- Keep IDs unique and document nesting valid; do not place interactive controls inside other interactive controls.
- Prefer native landmarks, headings, lists, tables, buttons, links, dialogs, and form controls before adding ARIA.
- Keep heading order meaningful and give each page a discoverable main heading without requiring every component fragment to own one.
- Use links for navigation and buttons for actions; set explicit button types inside forms.
- Use table headers and associations for data tables; use CSS layout rather than tables for presentation.
- Give embedded media and frames useful titles when their content is meaningful.
- Avoid obsolete elements, invalid attributes, duplicate metadata, and document-level claims based on isolated component fragments.

## Accessibility

- Every interactive control needs an accessible name, operable keyboard behavior, visible focus, and a logical focus order.
- Associate labels, descriptions, help, validation errors, and required/invalid states with their controls programmatically.
- Do not use color, position, shape, sound, or motion as the only way to communicate meaning.
- Preserve browser zoom and text resizing; verify reflow at narrow widths and high zoom without two-dimensional scrolling for ordinary content.
- Provide skip navigation and reliable landmarks for repeated page chrome when the page structure warrants them.
- Make dialogs announce a useful name, contain focus while open, restore focus when closed, and support expected dismissal behavior.
- Ensure menus, tabs, accordions, comboboxes, carousels, and custom widgets implement the complete interaction pattern, not only ARIA roles.
- Meet contrast requirements for text, controls, states, and focus indicators; verify disabled-state communication separately.
- Respect reduced motion, avoid dangerous flashing, and provide pause/stop controls for persistent moving or auto-updating content.
- Keep touch targets usable and separated; do not require precision gestures when a simpler alternative can exist.
- Announce important async status changes without unexpectedly moving focus.
- Test keyboard-only operation and at least one browser accessibility tree or screen-reader path for critical flows.

## CSS and responsive behavior

- Prevent unintended horizontal page overflow and clipped focus indicators across supported breakpoints.
- Prefer resilient layout primitives, intrinsic sizing, logical properties, and content-driven breakpoints over device-specific coordinates.
- Keep selector specificity low and predictable; avoid unnecessary `!important`, deep coupling to DOM shape, and unexplained magic values.
- Make hover-only information available to keyboard and touch users.
- Use `:focus-visible` without removing the native outline unless a reliable visible replacement exists.
- Animate transform and opacity for simple effects when practical; avoid layout-triggering properties in continuous animation.
- Use `will-change` sparingly and remove it when the promotion is no longer useful.
- Verify long text, localization expansion, reduced motion, forced colors, print output, and narrow containers when applicable.
- Avoid hiding essential content solely to make a breakpoint fit.

## Images, icons, and media

- Give meaningful images concise alternative text; use empty alt for decorative images and avoid duplicating adjacent visible labels.
- Reserve stable media space with intrinsic dimensions or an equivalent aspect-ratio container when layout shift is plausible.
- Serve appropriately sized responsive images and modern formats when the measured payload justifies it.
- Lazy-load offscreen media, but do not delay likely above-the-fold or largest-contentful content.
- Keep icons labeled when they are the only content of a control; hide purely decorative icons from assistive technology.
- Supply captions, transcripts, or audio descriptions according to the information the media conveys.
- Avoid putting essential text in images when real text can express it.
- Verify cropping, focal point, orientation, pixel density, failure states, and user-uploaded content constraints.

## Forms

- Use the correct input type, name, label, autocomplete token, input mode, and browser-friendly value semantics.
- Do not block paste or password managers without a demonstrated security requirement.
- Validate at the correct boundary and preserve user input after recoverable failures.
- Put actionable error text near the field, associate it programmatically, and provide a summary/focus strategy for long forms.
- Do not mark a field required unless the product contract requires it; communicate optional fields consistently.
- Keep submit behavior explicit and prevent accidental double submission while preserving progress and retry paths.
- Use client-side submission without `action`/`method` when that behavior is intentional and correctly implemented.
- Provide recovery for timeouts, expired sessions, network errors, partial success, and destructive actions.

## JavaScript and application behavior

- Avoid unsafe dynamic execution, unchecked HTML injection, prototype pollution surfaces, and trust in client-only validation.
- Handle promise rejection, cancellation, stale responses, race conditions, and component teardown for async work.
- Batch DOM reads and writes; avoid forced synchronous layout and per-frame application-state churn.
- Remove unused listeners, observers, timers, subscriptions, object URLs, and retained closures.
- Use feature detection and progressive enhancement rather than user-agent assumptions.
- Keep runtime validation at untrusted boundaries even when TypeScript types exist.
- Avoid unnecessary global state and global namespace mutation.
- Provide deterministic loading, empty, error, offline, disabled, success, optimistic, and rollback states where applicable.
- Preserve navigation history, URL state, focus, and scroll behavior for client-routed flows.

## Performance

- Set a route-appropriate budget for transferred bytes, JavaScript execution, fonts, images, and core user journeys.
- Measure before optimizing; distinguish lab metrics, field data, server latency, network cost, and main-thread work.
- Minimize render-blocking resources and critical request chains; preload or preconnect only when evidence supports them.
- Split or defer code by route/feature/visibility while avoiding waterfalls and duplicate dependencies.
- Keep third-party scripts deliberate, delayed where possible, sandboxed when appropriate, and observable in the budget.
- Prevent layout shifts from media, fonts, injected content, ads, consent UI, and late client rendering.
- Optimize likely LCP content without lazy-loading it; reduce long tasks and interaction latency in critical flows.
- Cache immutable assets safely, validate revalidation behavior, and avoid service-worker strategies that serve stale or broken application shells.
- Verify production builds and realistic low-end/mobile conditions rather than relying only on development mode.

## Security

- Never expose secrets, privileged tokens, private endpoints, stack traces, or sensitive source maps to public clients.
- Treat all user-controlled HTML, URLs, CSS, filenames, redirects, and message events as untrusted.
- Use secure transport and appropriate CSP, framing, referrer, permissions, and MIME-sniffing controls at the owning server layer.
- Protect new-tab external links when opener isolation is not otherwise guaranteed.
- Use secure, HttpOnly, SameSite cookies for server-managed sessions; avoid durable browser storage for high-value credentials.
- Validate postMessage origins and payloads; constrain iframe permissions and sandbox capabilities.
- Pin and review third-party dependencies/scripts, use integrity controls where operationally appropriate, and maintain an update process.
- Keep authentication, authorization, rate limiting, and sensitive validation on trusted server boundaries.
- Avoid leaking personal or secret values through URLs, analytics, logs, error reporting, or autocomplete behavior.

## Metadata and SEO

- Audit metadata only in the route/layout/file that owns it, including framework metadata APIs.
- Give indexable pages unique, descriptive titles and useful descriptions; keep canonical URLs consistent with routing policy.
- Align robots directives, sitemap entries, redirects, status codes, and canonical targets; do not include blocked or non-indexable URLs in sitemaps.
- Provide Open Graph/social metadata when sharing quality is a product requirement and ensure the referenced assets are reachable and correctly sized.
- Use structured data only when visible content supports it and validate the generated result.
- Preserve crawlable links and meaningful anchor text; avoid internal nofollow and redirect chains without a reason.
- Handle pagination, alternate languages, trailing slashes, query parameters, and duplicate routes through one documented URL policy.
- Render useful error/status pages with correct HTTP semantics.

## Privacy

- Collect only necessary personal data and document its purpose, retention, sharing, and deletion behavior.
- Obtain consent before non-essential tracking where required and ensure refusal is as usable as acceptance.
- Make privacy controls accessible, reversible, and consistent across devices or sessions when promised.
- Avoid third-party cookies, fingerprinting, or cross-context identifiers unless explicitly authorized and legally reviewed.
- Support access, correction, export, and erasure flows according to the product's obligations; do not infer a legal obligation from a code fragment.

## Internationalization

- Keep user-visible strings out of component logic when the project uses localization resources.
- Use locale-aware formatting for dates, times, numbers, currencies, units, lists, and plural forms.
- Preserve language/direction metadata and support right-to-left layout with logical CSS properties.
- Allow text expansion, varied word order, non-Latin input, grapheme clusters, and Unicode-safe truncation/search.
- Do not build sentences by concatenating translated fragments when translators need grammatical control.

## Testing and release evidence

- Test the happy path plus relevant loading, empty, failure, retry, cancellation, timeout, disabled, and partial-success paths.
- Cover keyboard operation, focus movement, accessible names, validation announcements, and responsive reflow for critical journeys.
- Test supported browsers and representative mobile/low-power conditions at the risk level of the change.
- Keep unit tests for logic, component tests for interaction contracts, and E2E tests for a small set of valuable journeys.
- Avoid brittle tests tied only to implementation detail or generated wording; assert observable behavior and meaningful invariants.
- Check console errors, failed requests, hydration warnings, unhandled rejections, memory leaks, and production-build behavior.
- Record the exact commands, routes, viewports, fixtures, and limitations used as completion evidence.

## False-positive filter

Before raising a finding, confirm that the inspected artifact owns the concern, the user impact is plausible, and an explicit safe pattern does not apply. Prefer one supported high-impact issue over many preference-level suggestions. When code context cannot prove the claim, state the missing evidence and the verification needed.
