# Application UI Quality Checklist

Use this reference for authenticated, API-driven applications, especially realtime/chat interfaces and workflows backed by multiple services. It supplements the portable web checklist; it does not own component architecture or backend design.

## Contract and reachability

- Confirm the feature is reachable from a real route, menu, control, notification, deep link, or documented entry point.
- Read the actual request, response, error, pagination, upload, realtime, and authorization contracts through the real client boundary or Gateway.
- Map each backend status to a deliberate UI state. Do not collapse forbidden, not found, conflict, validation, throttling, dependency failure, and timeout into one generic error.
- Preserve correlation or operation identifiers when the UI needs polling, support diagnostics, or distributed-operation tracking.
- Validate untrusted API and realtime payloads at runtime when malformed data would corrupt state or break a critical flow.

## State model

- Define idle, loading, refreshing, empty, populated, submitting, accepted/pending, completed, partial, failed, offline, stale, cancelled, and retrying states that can actually occur.
- Keep initial loading distinct from background refresh so existing usable content does not disappear unnecessarily.
- Make stale or partially synchronized data understandable without presenting it as confirmed server truth.
- Preserve user input and recoverable work across validation, network, session, and dependency failures.
- Prevent impossible combinations such as success plus active error, duplicated pending items, or controls enabled for unauthorized actions.

## Mutations and optimistic behavior

- Capture the exact pre-mutation snapshot needed for rollback; do not reconstruct it from already-mutated state.
- Give each client mutation a stable identity so duplicate clicks, retries, late responses, and echoed realtime events can converge.
- Disable or serialize only the conflicting action; avoid freezing unrelated UI while one mutation is pending.
- Reconcile the optimistic object with canonical server IDs, timestamps, ordering, permissions, derived fields, and moderation state.
- Handle late success after local cancellation, late failure after another update, and responses arriving in a different order than requests.
- Show when an operation is merely accepted for processing. Do not display business completion until completion evidence arrives.
- Make rollback visible and actionable when the optimistic result was already shown to the user.

## Realtime and cache convergence

- Establish one intentional subscription per scope and clean it up on unmount, logout, account switch, route change, and reconnect.
- Verify React development/Strict Mode does not create duplicate connections, listeners, timers, messages, or side effects.
- Deduplicate realtime events against mutation responses and previously handled event/message IDs.
- Define behavior for duplicate, missing, stale, and out-of-order events; use server versions or sequence data when available.
- Reconnect with bounded backoff and jitter, restore authentication, resubscribe, and fetch a recovery snapshot or missed range.
- Keep server cache, normalized entities, feature state, unread counts, badges, search results, and visible lists consistent after events.
- Avoid blindly appending events when the item may already exist, have moved, been edited, or been deleted.
- Remove sensitive cached/realtime state on logout or identity/workspace change.

## Chat and timeline interfaces

- Preserve stable message identity across local pending, sent, delivered, read, edited, failed, retried, and deleted states.
- Keep chronological ordering deterministic when client time differs from server time or history pages arrive around live messages.
- Avoid scroll jumps when prepending history, loading media, receiving new messages, editing content, or showing typing indicators.
- Auto-scroll only when the user is already near the newest content; otherwise expose a clear new-message affordance.
- Make delivery/read status accessible without relying only on icon shape or color.
- Handle reply targets, mentions, reactions, edits, deletions, attachments, and thread context when their source item is unavailable.
- Rate-limit ephemeral typing/presence signals, expire stale signals, and never persist them as durable truth.
- Virtualized lists must preserve keyboard access, focus, measurement stability, accessible semantics, and restored scroll position.

## Uploads and attachments

- Validate type, size, count, filename, and preview behavior before upload while treating server validation as authoritative.
- Model queued, hashing/preparing, uploading, processing/scanning, completed, failed, cancelled, and retrying states when applicable.
- Show per-item progress and failure in multi-file operations; do not erase successful items because one item failed.
- Support cancellation and cleanup of requests, previews, object URLs, temporary records, and orphaned client state.
- Keep attachment identity stable when a local preview is replaced by the server object.
- Verify expired URLs, unavailable media, unsupported previews, slow networks, duplicate selection, and retry after session refresh.
- Do not expose local paths, secret storage URLs, tokens, or sensitive metadata in rendered markup, logs, or analytics.

## Authentication and authorization UX

- Distinguish unauthenticated, expired session, forbidden action, missing membership, and temporarily unavailable identity dependencies.
- Preserve safe return navigation and recoverable form state across login or session renewal.
- Hide or disable unauthorized controls for clarity, but rely on server authorization for enforcement.
- Handle permission changes delivered while the screen is open; remove inaccessible data and close or downgrade active editors safely.
- Avoid redirect loops, repeated refresh storms, and concurrent token-renewal races.
- Clear account-specific queries, stores, subscriptions, drafts, and sensitive browser state when identity changes.

## Interaction and accessibility

- Move focus intentionally after opening/closing overlays, adding/removing items, route transitions, destructive actions, and validation failures.
- Announce mutation progress and meaningful completion/failure without flooding live regions during frequent realtime updates.
- Keep keyboard order and shortcuts predictable in message composers, emoji/reaction pickers, attachment menus, dialogs, and virtualized lists.
- Prevent global shortcuts while the user is typing or using assistive technology controls.
- Make destructive scope explicit, especially when “remove for me”, “delete for everyone”, leave, dissolve, revoke, and cancel are different operations.
- Preserve responsive usability for split panes, drawers, virtual keyboards, safe areas, long localized labels, and zoomed text.

## Failure and recovery matrix

For each critical flow, exercise the failures that the contract can produce:

- client validation and server validation;
- unauthenticated and forbidden;
- missing/deleted dependency;
- conflict or stale version;
- payload/type/size rejection;
- throttling with retry guidance;
- offline, timeout, cancellation, and DNS/network failure;
- Gateway or downstream 5xx;
- accepted operation that later fails;
- realtime disconnect during an in-flight mutation;
- duplicate retry and late response after navigation.

Verify both visible UX and final server/cache/realtime state. A toast alone is not proof of recovery.

## Browser proof

- Exercise the complete click path from a real entry point at representative desktop and mobile widths.
- Inspect rendered semantics, focus, live announcements, scroll behavior, console, network requests, status bodies, and subscription count.
- Throttle network or force contract-level failures to prove loading, retry, rollback, and late-response behavior.
- Verify at least one reconnect/resubscribe path for realtime work and one optimistic rollback path for optimistic work.
- Confirm production-build behavior; development mode can hide bundle, caching, hydration, and duplicate-effect defects.
- Record the route, account/role, fixtures, viewport, commands, observed states, and anything not exercised.

## Finding priority

Treat data exposure, authorization confusion, lost user work, incorrect destructive scope, duplicated mutations, false completion, unrecoverable state divergence, and inaccessible critical interaction as high impact. Treat cosmetic consistency or hypothetical micro-optimization as lower priority unless measured evidence shows user harm.
