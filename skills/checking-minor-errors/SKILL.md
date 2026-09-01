---
name: checking-minor-errors
description: Automates checking and fixing minor errors across microservices, such as encoding issues, hardcoded strings (Rule 5 violations), and compilation warnings. Triggers when the user asks to "rà soát lỗi" (scan for errors).
---

# Checking for Minor Errors

This skill provides an automated workflow to scan and fix minor errors in the BridgeChat microservices architecture. It ensures compliance with codebase rules, specifically encoding standards (UTF-8 CRLF) and hardcoded logging/exception string rules (Rule 5).

## Triggers
This skill should be activated when the user requests:
- `rà soát lỗi tất cả` (scan all services for errors)
- `rà soát lỗi [tên service]` (scan a specific service for errors)

## Automated Workflow (The Flow)

When this skill is triggered, you MUST execute the following steps in order. All scripts are located in `.agents/skills/checking-minor-errors/scripts/`.

### Step 1: Format Encoding, Line Endings & JSON Structure
Run the formatting scripts to enforce UTF-8 encoding, CRLF line endings, and clean standard JSON indentation across the target service(s):
- `python clean_mojibake.py <target_dir>`: Quét và khôi phục triệt để lỗi mã hóa ký tự (Mojibake / Double-encoded UTF-8) trong các comment và chuỗi ký tự tiếng Việt.
- `python format_encoding_eol.py <target_dir>`: Enforces UTF-8 without BOM and CRLF line endings on all source files.
- `python format_json.py <target_dir>`: Standardizes and formats all JSON (`appsettings*.json`, `launchSettings.json`, locale files) with 2-space indentation and CRLF.

### Step 2: Validate AGENTS.md Architectural Rules (Rules 1-5)
Run the dedicated Python scripts to detect any architectural or coding standard violations:
- `python scan_rule1.py <target_dir>`: Scans for Dapper/EFCore violations (Rule 1).
- `python scan_rule2.py <target_dir>`: Scans for REST API parameter violations (Rule 2).
- `python scan_rule3.py <target_dir>`: Scans for CQRS/VSA naming and structure rules (Rule 3).
- `python scan_rule4.py <target_dir>`: Scans for Fully Qualified Name restrictions (Rule 4).
- `python audit_rule4.py <target_dir>`: Comprehensive Rule 4 audit (Encoding, EOL, Vietnamese XML comments, forbidden tags, FQN).
- `python scan_rule5.py <target_dir>`: Scans for Localization and Hardcoded string violations (Rule 5).
- `python scan_raw_localizer_strings.py`: Quét toàn bộ mã nguồn C# để phát hiện mọi chuỗi raw string trong `_localizer["..."]` (bao gồm E2EE, dot notation và tham số format).
- `python fix_raw_localizer_strings.py`: Tự động chuyển đổi `_localizer["KEY"]` sang `_localizer[LocalizationKeys.Identifier]`, bổ sung using namespace và bảo đảm UTF-8 CRLF.
- `python audit_localization_keys.py`: Rà soát raw `_localizer["KEY"]` trong các service backend, đối chiếu ba locale và gợi ý `LocalizationKeys.*`. Thêm `--fix` để tự chuyển đổi.

- If ANY violations are found in the above scripts, STOP the flow, present the violations to the user, and ask for further instructions on how to fix them.

### Step 3: Build and Verify
If no violations are found (or after fixing them), verify the compilation integrity.
- If scanning ALL services, run: `powershell -ExecutionPolicy Bypass -File build_all.ps1`
- If scanning a SPECIFIC service, run the `dotnet build` command for that service with the `/warnaserror` flag.

### Step 4: Report
Provide a concise, Vietnamese report to the user confirming the status of the formatting, the architecture rule scans, and the build results.

### Step 5: Git Commit & Push (Multi-repo Sync)
To synchronize, commit and push changes across all microservices, shared libraries, and web frontend:
- `python push_all.py --status`: Checks the git status across all 12 repositories.
- `python push_all.py -m "your commit message"`: Automatically commits and pushes changed repositories to `origin/master` with retry support.

## Extending the Skill
If you write new Python scripts for minor error checking or fixing in the future, save them in `.agents/skills/checking-minor-errors/scripts/` and update this `SKILL.md` file to include them in the automated workflow.
