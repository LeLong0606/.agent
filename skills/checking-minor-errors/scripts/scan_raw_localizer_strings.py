#!/usr/bin/env python3
"""
Quét và phát hiện tất cả các lệnh gọi _localizer[...] hoặc localizer[...]
sử dụng chuỗi cứng (string literal như "E2EE.BACKUP_VERSION_CONFLICT", "USER_NOT_FOUND")
thay vì sử dụng LocalizationKeys.* có kiểu mạnh.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
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

# Regex bắt mọi trường hợp localizer["raw_key"] hoặc _localizer["raw_key", args...]
RAW_LOCALIZER_PATTERN = re.compile(
    r'(?P<localizer>\b(?:_?[A-Za-z0-9_]*localizer[A-Za-z0-9_]*))'
    r'\s*\[\s*"(?P<key>[^"]+)"\s*(?P<args>,[^\]]*)?\]',
    re.IGNORECASE,
)


@dataclass(frozen=True)
class RawLocalizerFinding:
    service: str
    file_path: Path
    line_number: int
    full_expression: str
    key: str
    args: str | None
    in_resource: bool
    suggested_identifier: str | None


def configure_output() -> None:
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")


def to_pascal_case(key: str) -> str:
    """Chuyển chuỗi KEY_NAME hoặc KEY.NAME thành PascalCase (tương thích LocalizationKeys generator)."""
    parts = [part for part in re.split(r"[^A-Za-z0-9]+", key) if part]
    identifier = "".join(part[0].upper() + part[1:].lower() for part in parts)
    return f"Key{identifier}" if identifier and identifier[0].isdigit() else identifier


def load_all_resource_keys(root: Path) -> dict[str, str]:
    """Tải toàn bộ resource keys từ 3 tệp JSON trung tâm và ánh xạ sang định danh C#."""
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


def scan_csharp_files(root: Path, services: list[str], known_keys: dict[str, str]) -> list[RawLocalizerFinding]:
    findings: list[RawLocalizerFinding] = []

    for service in services:
        service_dir = root / service
        if not service_dir.is_dir():
            continue

        for current_root, dirs, files in os.walk(service_dir):
            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRECTORIES]
            for file in files:
                if not file.endswith(".cs"):
                    continue

                file_path = Path(current_root) / file
                try:
                    content = file_path.read_text(encoding="utf-8-sig")
                except Exception:
                    continue

                for match in RAW_LOCALIZER_PATTERN.finditer(content):
                    key = match.group("key")
                    args = match.group("args")
                    line_no = content.count("\n", 0, match.start()) + 1
                    full_expr = match.group(0)

                    in_res = key in known_keys
                    sugg_id = known_keys.get(key, to_pascal_case(key))

                    findings.append(
                        RawLocalizerFinding(
                            service=service,
                            file_path=file_path,
                            line_number=line_no,
                            full_expression=full_expr,
                            key=key,
                            args=args,
                            in_resource=in_res,
                            suggested_identifier=sugg_id,
                        )
                    )

    return findings


def print_report(root: Path, findings: list[RawLocalizerFinding]) -> None:
    print("=" * 95)
    print("  QUÉT TẤT CẢ LỖI GỌI RAW STRING TRONG _localizer[...] (RULE 5)")
    print("=" * 95)

    if not findings:
        print("[OK] Không phát hiện bất kỳ chuỗi raw string nào trong _localizer[...]. 100% tuân thủ!")
        print("=" * 95)
        return

    by_service: dict[str, list[RawLocalizerFinding]] = {}
    for f in findings:
        by_service.setdefault(f.service, []).append(f)

    for service, items in by_service.items():
        print(f"\n[{service}] - {len(items)} vi phạm:")
        for item in items:
            rel_path = item.file_path.relative_to(root)
            status = "[ĐÃ CÓ TRONG JSON]" if item.in_resource else "[CHƯA CÓ TRONG JSON - CẦN THÊM]"
            suggestion = f"LocalizationKeys.{item.suggested_identifier}"
            args_str = f" với tham số: {item.args.strip()}" if item.args else ""
            print(f"  - {rel_path}:{item.line_number} -> {item.full_expression}")
            print(f"    Key: \"{item.key}\" | Trạng thái: {status} | Đề xuất: {suggestion}{args_str}")

    print("\n" + "-" * 95)
    print(f"TỔNG SỐ RAW LOCALIZER STRINGS: {len(findings)}")
    missing_in_json = [f for f in findings if not f.in_resource]
    print(f"SỐ KEY CHƯA KHAI BÁO TRONG 3 FILE RESOURCE JSON: {len(missing_in_json)}")
    if missing_in_json:
        unique_missing = sorted(set(f.key for f in missing_in_json))
        print(f"Danh sách key còn thiếu:")
        for k in unique_missing:
            print(f"  * \"{k}\"")
    print("=" * 95)


def main() -> int:
    configure_output()
    parser = argparse.ArgumentParser(
        description="Quét toàn bộ chuỗi raw string được truyền vào _localizer[...] thay vì LocalizationKeys.*."
    )
    default_root = Path(__file__).resolve().parents[4]
    parser.add_argument("--root", type=Path, default=default_root, help="Thư mục gốc BridgeChat.")
    parser.add_argument(
        "--services",
        nargs="+",
        default=list(DEFAULT_SERVICES),
        help="Danh sách service cần quét.",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    known_keys = load_all_resource_keys(root)
    findings = scan_csharp_files(root, args.services, known_keys)
    print_report(root, findings)

    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
