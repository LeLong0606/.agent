---
name: bridgechat-text-integrity
description: Mandatory gate for mojibake, lossy Vietnamese, localization ownership, UTF-8 without BOM, and CRLF.
version: 3.0.0
requires_skills: checking-minor-errors, i18n-localization
artifact_outputs: text-integrity-report, encoding-report, rule4-audit
---

# /bridgechat-text-integrity — Text and encoding gate

$ARGUMENTS

Run after every write wave and before completion.

Localization ownership is strict:
- Frontend UI translations: bridgechatwebreact/public/locales/** only.
- Backend API/log/validation resources: BridgeChat.SharedLibraries/Core.Localization/Resources/en-US.json, vi-VN.json, and zh-CN.json only.
- Backend hover metadata must be regenerated from backend resources/templates. Never hand-edit Generated/LocalizationKeys.g.cs.

Treat valid-UTF-8 but damaged text as failure, including mojibake markers, replacement/NUL characters, or lossy Vietnamese such as MA tAi, Ting Vit, MTt tin nhn, tTp Anh kAm, and khA'ng kh>p.

Required loop on changed scope:
1. clean_mojibake.py target
2. format_encoding_eol.py target
3. format_json.py target when JSON changed
4. Regenerate localization output when source/template changed
5. Search suspicious markers and inspect changed passages
6. format_encoding_eol.py target again after the final write
7. audit_rule4.py target
8. audit_localization_keys.py for backend localization
9. Repeat until two consecutive passes produce no diff

PASS requires strict UTF-8 decode, no BOM, no bare LF, no replacement/NUL character, no suspicious text, and stable regeneration.
