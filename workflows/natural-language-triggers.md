# Natural-Language Workflow Triggers

This catalog documents representative Vietnamese natural-language requests that route workflows. Matching is semantic, not exact-string based: users may change tense, pronouns, word order, filenames, services, routes, or feature names without losing the intended route.

`EXISTING` means the intent was already covered by a workflow before the generic workflow expansion. `NEW` means routing was added or made explicit in this expansion.

## Routing precedence

1. If the request names BridgeChat, `bridgechatwebreact`, `BridgeChat.*`, or a known BridgeChat service, use BridgeChat intake and project workflows.
2. Otherwise use generic request intake and shared workflows.
3. Explicit report-only, plan-only, verification-only, no-code, migration, refactor, or UI-polish wording overrides a broader “làm/triển khai” verb.
4. Destructive, production, deployment, commit, push, or external mutation wording still requires the applicable authorization boundary.

# Shared workflow triggers

## `request-intake` — NEW

Usually automatic for any non-BridgeChat engineering request. Direct examples:

- “Phân tích yêu cầu này rồi chọn workflow phù hợp.”
- “Xem task này thuộc backend, frontend hay full-stack.”
- “Đọc yêu cầu và tự route giúp tôi.”
- “Xác định phạm vi, rủi ro và definition of done trước khi làm.”
- “Tôi mô tả tự nhiên, bạn tự chọn skill và workflow nhé.”

## `build-feature` — NEW shared workflow

- “Làm tính năng này từ đầu đến cuối.”
- “Implement feature này cho dự án.”
- “Thêm chức năng quản lý thành viên.”
- “Xây API và nối luôn frontend.”
- “Hoàn thiện luồng này cả backend lẫn UI.”
- “Tạo endpoint, business logic, lưu dữ liệu và test.”
- “Build feature theo conventions hiện có.”
- “Làm product slice này hoàn chỉnh.”
- “Thêm integration này và kiểm tra end-to-end.”
- “Tiếp tục triển khai feature trong plan đã duyệt.”

## `build-ui` — NEW shared workflow

- “Làm màn hình này cho tôi.”
- “Xây giao diện React cho tính năng này.”
- “Tạo trang mới và nối API thật.”
- “Implement modal này đầy đủ trạng thái.”
- “Làm UI responsive cho desktop và mobile.”
- “Thêm form này với validation và error state.”
- “Biến component này thành một flow dùng được thật.”
- “Làm dashboard này theo design system hiện có.”
- “Tạo UI có loading, empty, error và retry.”
- “Nối giao diện này vào route và entry point thật.”

## `fix-error` — NEW shared workflow

- “Sửa lỗi này giúp tôi.”
- “Điều tra tại sao test này fail rồi sửa.”
- “API đang trả 500, tìm nguyên nhân và fix.”
- “Màn hình này bị trắng sau khi đăng nhập.”
- “Bug này lúc có lúc không, trace giúp tôi.”
- “Tìm root cause chứ đừng vá triệu chứng.”
- “Fix regression này và thêm test chống tái phát.”
- “Request này trả sai status code.”
- “Dữ liệu bị stale sau khi refresh.”
- “Build đang fail ở bước này, xử lý hoàn chỉnh.”

## `safe-refactor` — NEW

- “Refactor phần này nhưng không đổi behavior.”
- “Tách class này ra cho sạch mà giữ nguyên contract.”
- “Chuyển logic sang service/hook phù hợp.”
- “Dọn god component này nhưng không thêm tính năng.”
- “Tái cấu trúc module này an toàn.”
- “Đổi ownership của đoạn code này mà không phá caller.”
- “Gộp phần code trùng này và chứng minh không regression.”
- “Rename/reorganize phần này nhưng giữ tương thích.”
- “Làm sạch technical debt trong phạm vi này.”
- “Refactor theo conventions hiện tại, đừng opportunistic rewrite.”

## `migration` — NEW

- “Migration schema này giúp tôi.”
- “Chuyển dữ liệu từ cấu trúc cũ sang mới.”
- “Nâng dependency này mà giữ tương thích.”
- “Đổi API contract theo kiểu rollout an toàn.”
- “Version event này mà consumer cũ vẫn chạy.”
- “Chuyển config/protocol này sang bản mới.”
- “Lập kế hoạch expand-migrate-contract.”
- “Backfill dữ liệu này có resume và rollback.”
- “Thiết kế mixed-version deployment cho thay đổi này.”
- “Bỏ legacy field này sau một compatibility window.”

## `verify` — NEW shared workflow

- “Kiểm tra những thay đổi này.”
- “Review và xác nhận task đã hoàn thành chưa.”
- “Chỉ verify, không sửa code.”
- “Chạy test/build/lint và báo PASS hay FAIL.”
- “Kiểm chứng behavior này qua runtime.”
- “Xem diff có regression hoặc sai contract không.”
- “Audit phần vừa làm và đưa bằng chứng.”
- “Kiểm tra lại trước khi bàn giao.”
- “Xác minh bug này thực sự đã hết.”
- “Cho tôi báo cáo verification, đừng nói ‘looks fine’.”

## `frontend-quality-gate` — EXISTING

- “Audit frontend này.”
- “Kiểm tra accessibility cho component này.”
- “Review chất lượng UI trước khi hoàn thành.”
- “Kiểm tra responsive, focus và keyboard.”
- “Xem form này có lỗi semantics hoặc validation UX không.”
- “Kiểm tra optimistic rollback và realtime convergence.”
- “Review loading, empty, error và retry states.”
- “Chạy frontend quality gate.”
- “Kiểm tra UI này có false-positive checklist nào không.”
- “Audit route này theo Front-End Checklist.”

## `media-production` — NEW

- “Làm video giới thiệu sản phẩm này.”
- “Biến PR này thành video giải thích.”
- “Tạo motion graphic ngắn cho số liệu này.”
- “Thêm caption vào video này.”
- “Làm faceless explainer từ nội dung này.”
- “Tạo slideshow/pitch deck có chuyển động.”
- “Recut video talking-head và thêm graphic overlay.”
- “Làm video theo nhạc này.”
- “Port composition Remotion này sang HyperFrames.”
- “Xử lý media, voiceover, BGM hoặc background removal cho project này.”

# BridgeChat primary workflow triggers

Every phrase below automatically runs `bridgechat-request-intake` first.

## `bridgechat-build-feature` — EXISTING

- “Làm tính năng xoá tin nhắn cho BridgeChat.”
- “Thêm chức năng quản lý nhóm vào BridgeChat.”
- “Implement feature này xuyên qua các service.”
- “Xây backend cho luồng gửi attachment.”
- “Thêm API, event và consumer cho tính năng này.”
- “Làm full-stack feature này trong BridgeChat.”
- “Nối MessageService, ConnectionService và frontend cho flow này.”
- “Thêm business flow này qua Gateway.”
- “Hoàn thiện Saga cho nghiệp vụ này.”
- “Build feature theo CQRS/VSA và Dapper của BridgeChat.”

## `bridgechat-build-ui` — EXISTING

- “Làm giao diện tính năng này trong bridgechatwebreact.”
- “Tạo modal xoá hội thoại cho BridgeChat.”
- “Nối màn hình này vào API Gateway thật.”
- “Làm UI chat này đầy đủ loading và error state.”
- “Thêm entry point cho feature này trong React app.”
- “Implement optimistic update và rollback cho thao tác này.”
- “Làm màn hình quản lý thành viên nhóm.”
- “Thêm UI upload attachment có progress và retry.”
- “Làm responsive mobile/desktop cho màn hình này.”
- “Xử lý realtime reconnect và dedup trên UI.”

## `bridgechat-fix-error` / `bridgechat-debug` — EXISTING

- “BridgeChat đang lỗi 500 ở endpoint này, sửa giúp tôi.”
- “Gateway trả 404 nhưng service có route, trace đi.”
- “Tin nhắn bị duplicate sau reconnect.”
- “Message bị mất nhưng không có exception.”
- “UI báo thành công nhưng backend chưa hoàn tất.”
- “Saga bị kẹt ở trạng thái pending.”
- “Consumer xử lý event hai lần.”
- “Attachment upload xong nhưng UI không cập nhật.”
- “Đăng xuất rồi đăng nhập lại thì dữ liệu biến mất.”
- “Fix race condition này và thêm regression test.”
- “Trace lỗi từ frontend qua Gateway xuống service.”
- “Tìm root cause theo correlation ID này.”

## `bridgechat-investigate` — EXISTING

- “Chỉ điều tra lỗi này, chưa sửa code.”
- “Phân tích nguyên nhân và báo cáo cho tôi.”
- “Trace luồng này qua các service nhưng không thay đổi gì.”
- “Xem service nào sở hữu dữ liệu này.”
- “Điều tra event này đang được producer/consumer nào dùng.”
- “Kiểm tra contract thật qua Gateway.”
- “Tìm nơi gây stale cache nhưng chỉ báo cáo.”
- “Đọc log và dựng timeline sự cố.”
- “Xác minh giả thuyết này trước khi implement.”
- “Cho tôi root-cause report, no code changes.”

## `bridgechat-plan` — EXISTING

- “Lập kế hoạch cho feature này, chưa code.”
- “Viết implementation plan cho BridgeChat.”
- “Phân rã task này theo service và file.”
- “Cho tôi plan rollout và deploy order.”
- “Thiết kế contract/API/event trước khi làm.”
- “Lập kế hoạch Saga và recovery.”
- “Plan frontend/backend handoff cho feature này.”
- “Đánh giá phạm vi rồi viết plan reviewable.”
- “Chỉ lên kế hoạch, chờ tôi duyệt.”
- “Viết file-level plan cho thay đổi này.”

## `bridgechat-implement` — EXISTING

- “Implement plan BridgeChat đã duyệt.”
- “Bắt đầu code theo kế hoạch này.”
- “Tiếp tục triển khai từ plan hiện tại.”
- “Thực hiện các wave trong plan.”
- “Code phần backend theo contract đã thống nhất.”
- “Triển khai phần còn lại, giữ nguyên scope plan.”
- “Apply plan này vào repository.”
- “Làm tiếp implementation, không cần brainstorm lại.”

## `bridgechat-verify` — EXISTING

- “Verify thay đổi BridgeChat này.”
- “Review task này đã xong chưa.”
- “Chạy build/test và kiểm tra runtime flow.”
- “Kiểm tra localization ownership và encoding.”
- “Xác minh qua Gateway và UI.”
- “Chỉ verify, không sửa.”
- “Audit diff này theo architecture BridgeChat.”
- “Kiểm tra event/realtime contract sau thay đổi.”
- “Báo PASS/FAIL với command evidence.”
- “Kiểm tra trước khi handoff.”

## `bridgechat-handoff` — EXISTING

- “Lập handoff cho phần vừa làm.”
- “Tóm tắt thay đổi để frontend/backend tiếp tục.”
- “Viết báo cáo bàn giao BridgeChat.”
- “Cho tôi contract và remaining work.”
- “Tổng hợp deploy order, risks và pending items.”
- “Bàn giao feature này cho agent khác.”
- “Tạo frontend handoff từ backend changes.”
- “Tóm tắt service impact và verification evidence.”

# BridgeChat workflows added in this expansion

## `bridgechat-migrate` — NEW

- “Migration database của MessageService.”
- “Chuyển schema này trong BridgeChat mà không downtime.”
- “Version integration event này và giữ consumer cũ chạy.”
- “Đổi realtime contract theo rollout tương thích.”
- “Backfill dữ liệu hội thoại và cho phép resume.”
- “Nâng dependency dùng chung cho các service.”
- “Chuyển API contract qua Gateway sang version mới.”
- “Lập deploy order cho migration nhiều service.”
- “Bỏ legacy column sau compatibility window.”
- “Thiết kế rollback/forward recovery cho migration BridgeChat.”
- “Migrate config/broker protocol này an toàn.”
- “Chuyển dữ liệu owner mà không được ghi chéo database.”

## `bridgechat-refactor` — NEW

- “Refactor MessageService nhưng không đổi behavior.”
- “Tách handler này ra mà giữ nguyên API contract.”
- “Dọn controller này theo CQRS/VSA hiện tại.”
- “Chuyển SQL về Infrastructure repository.”
- “Refactor React hook này nhưng giữ realtime behavior.”
- “Tái cấu trúc flow này mà không đổi status code.”
- “Gộp code trùng giữa các handler nhưng không đổi event.”
- “Đổi ownership code này mà không ghi chéo database.”
- “Làm sạch technical debt trong BridgeChat, no feature changes.”
- “Refactor localization nhưng giữ đúng frontend/backend boundary.”
- “Tách god component trong bridgechatwebreact.”
- “Refactor theo từng wave và chứng minh không regression.”

## `bridgechat-ui-polish` — NEW

- “Polish màn hình chat này cho đẹp và dễ dùng hơn.”
- “Audit visual UI BridgeChat rồi sửa các vấn đề chính.”
- “Làm giao diện này bớt thô nhưng không đổi nghiệp vụ.”
- “Cải thiện hierarchy, spacing và typography màn hình này.”
- “Polish modal này trên desktop và mobile.”
- “Sửa UX loading/empty/error cho màn hình hiện có.”
- “Làm UI này accessible hơn và giữ nguyên API.”
- “Kiểm tra design consistency trong bridgechatwebreact.”
- “Thêm micro-interaction hợp lý cho thao tác này.”
- “Làm animation cho màn hình này nhưng phải hỗ trợ reduced motion.”
- “So sánh before/after bằng browser screenshot.”
- “Dọn responsive và long translation cho UI này.”

# Automatically chained BridgeChat workflows

These normally do not need direct invocation.

## `bridgechat-brain-context` — EXISTING automatic

Activated by any BridgeChat implementation, investigation, plan, refactor, migration, UI, or defect request. Direct wording also works:

- “Đọc brain context trước khi làm.”
- “Khôi phục walkthrough liên quan feature này.”
- “So sánh memory với source hiện tại.”

## `bridgechat-microservice-orchestration` — EXISTING automatic

Activated by language involving multiple services, events, Saga, broker, Outbox/Inbox, eventual consistency, cross-service contracts, realtime propagation, or deploy order:

- “Flow này đi qua nhiều service.”
- “Thiết kế Saga cho nghiệp vụ này.”
- “Map producer, consumer và realtime contract.”
- “Kiểm tra duplicate/out-of-order event.”
- “Lập deploy order cho thay đổi cross-service.”

## `bridgechat-text-integrity` — EXISTING automatic

Activated after BridgeChat writes and whenever localization, Vietnamese text, generated localization, encoding, mojibake, JSON resources, or CRLF is involved:

- “Kiểm tra mojibake và encoding.”
- “Thêm bản dịch frontend ba ngôn ngữ.”
- “Cập nhật backend localization resources.”
- “Chạy text-integrity gate.”
- “Kiểm tra UTF-8 no BOM và CRLF.”

## `bridgechat-skill-router` — EXISTING automatic

Activated by every BridgeChat request after intake. Direct wording:

- “Tự chọn skill phù hợp cho task BridgeChat này.”
- “Chỉ load bộ skill nhỏ nhất cần thiết.”
- “Route task này theo risk và scope.”

# Natural-language modifiers

These phrases modify the selected workflow rather than selecting a different domain workflow:

- “chỉ phân tích”, “chưa sửa”, “no code changes” → report-only investigation.
- “chỉ lập kế hoạch”, “chờ tôi duyệt” → plan-only.
- “chỉ verify”, “không được sửa” → verification with `verify-and-stop` behavior.
- “không đổi behavior”, “no feature changes” → safe refactor.
- “giữ backward compatibility”, “không downtime”, “mixed version” → migration depth.
- “làm từ đầu đến cuối”, “hoàn thiện luôn” → continue through implementation and verification.
- “qua Gateway thật”, “test runtime”, “browser proof” → require runtime evidence.
- “desktop và mobile”, “keyboard”, “screen reader” → frontend quality depth.
- “nhiều service”, “event”, “Saga”, “Outbox”, “Inbox”, “broker” → distributed orchestration.
- “commit”, “push”, “deploy”, “production”, “xoá dữ liệu” → retain explicit authorization and safety gates.
