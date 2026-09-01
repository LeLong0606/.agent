#!/usr/bin/env python3
"""
Tự động chuyển đổi các lệnh gọi _localizer["RAW_KEY"] sang _localizer[LocalizationKeys.PascalCase]
và tự động chèn 'using BridgeChat.SharedLibraries.Core.Localization;' nếu chưa có.
Đồng thời đảm bảo mã hóa UTF-8 không BOM và định dạng dòng CRLF.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

DEFAULT_SERVICES = (
    "BridgeChat.APIGateway",
    "BridgeChat.AttachmentService",
    "BridgeChat.ConnectionService",
    "BridgeChat.GroupService",
    "BridgeChat.IdentityService",
    "BridgeChat.MessageService",
    "BridgeChat.NotificationService",
    "BridgeChat.PresenceService",
    "BridgeChat.SearchService",
    "BridgeChat.UserService",
    "BridgeChat.SharedLibraries",
)

SUPPORTED_CULTURES = ("en-US", "vi-VN", "zh-CN")
EXCLUDED_DIRECTORIES = {"bin", "obj", ".git", ".vs", "Generated"}
LOCALIZATION_NAMESPACE = "BridgeChat.SharedLibraries.Core.Localization"

RAW_LOCALIZER_PATTERN = re.compile(
    r'(?P<localizer>\b(?:_?[A-Za-z0-9_]*localizer[A-Za-z0-9_]*))'
    r'\s*\[\s*"(?P<key>[^"]+)"\s*(?P<args>,[^\]]*)?\]',
    re.IGNORECASE,
)


def configure_output() -> None:
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")


def to_pascal_case(key: str) -> str:
    parts = [part for part in re.split(r"[^A-Za-z0-9]+", key) if part]
    identifier = "".join(part[0].upper() + part[1:].lower() for part in parts)
    return f"Key{identifier}" if identifier and identifier[0].isdigit() else identifier


def load_all_resource_keys(root: Path) -> dict[str, str]:
    resources_dir = root / "BridgeChat.SharedLibraries" / "Core.Localization" / "Resources"
    resources: dict[str, dict[str, str]] = {}

    for culture in SUPPORTED_CULTURES:
        res_file = resources_dir / f"{culture}.json"
        if not res_file.exists():
            continue
        with res_file.open("r", encoding="utf-8-sig") as f:
            resources[culture] = json.load(f)

    if not resources or "vi-VN" not in resources:
        return {}

    all_keys = set(resources["vi-VN"].keys())
    return {key: to_pascal_case(key) for key in all_keys}


def add_localization_using(source: str) -> str:
    using_statement = f"using {LOCALIZATION_NAMESPACE};"
    if using_statement in source or f"namespace {LOCALIZATION_NAMESPACE}" in source:
        return source

    using_matches = list(re.finditer(r"^using\s+[^;]+;\s*$", source, re.MULTILINE))
    if using_matches:
        insertion = using_matches[-1].end()
        return source[:insertion] + "\r\n" + using_statement + source[insertion:]

    return using_statement + "\r\n\r\n" + source


def fix_csharp_file(file_path: Path, known_keys: dict[str, str]) -> int:
    try:
        source = file_path.read_text(encoding="utf-8-sig")
    except Exception:
        return 0

    replacements = 0

    def replace_match(match: re.Match[str]) -> str:
        nonlocal replacements
        key = match.group("key")
        args = match.group("args") or ""
        localizer_name = match.group("localizer")

        if key not in known_keys:
            # Bỏ qua nếu key chưa có trong resource JSON để tránh compile error
            return match.group(0)

        replacements += 1
        identifier = known_keys[key]
        return f"{localizer_name}[LocalizationKeys.{identifier}{args}]"

    new_source = RAW_LOCALIZER_PATTERN.sub(replace_match, source)
    if replacements == 0:
        return 0

    # Bổ sung using nếu cần
    new_source = add_localization_using(new_source)

    # Đảm bảo CRLF
    normalized = new_source.replace("\r\n", "\n").replace("\r", "\n").replace("\n", "\r\n")
    file_path.write_text(normalized, encoding="utf-8", newline="")
    return replacements


def main() -> int:
    configure_output()
    parser = argparse.ArgumentParser(
        description="Tự động sửa toàn bộ _localizer[\"KEY\"] sang _localizer[LocalizationKeys.Identifier]."
    )
    default_root = Path(__file__).resolve().parents[4]
    parser.add_argument("--root", type=Path, default=default_root, help="Thư mục gốc BridgeChat.")
    parser.add_argument(
        "--services",
        nargs="+",
        default=list(DEFAULT_SERVICES),
        help="Danh sách service cần sửa.",
    )
    args = parser.parse_args()
    root = args.root.resolve()

    known_keys = load_all_resource_keys(root)
    total_fixed = 0

    for service in args.services:
        service_dir = root / service
        if not service_dir.is_dir():
            continue

        for current_root, dirs, files in os.walk(service_dir):
            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRECTORIES]
            for file in files:
                if not file.endswith(".cs"):
                    continue
                file_path = Path(current_root) / file
                count = fix_csharp_file(file_path, known_keys)
                if count > 0:
                    rel_path = file_path.relative_to(root)
                    print(f"Đã sửa {count} vị trí tại: {rel_path}")
                    total_fixed += count

    print(f"\nTổng số vị trí đã sửa thành công: {total_fixed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
