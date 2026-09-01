#!/usr/bin/env python3
"""Rà soát và chuyển raw localization key sang LocalizationKeys có IntelliSense."""

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
)
SUPPORTED_CULTURES = ("en-US", "vi-VN", "zh-CN")
EXCLUDED_DIRECTORIES = {"bin", "obj", ".git", ".vs"}
LOCALIZATION_NAMESPACE = "BridgeChat.SharedLibraries.Core.Localization"
LOCALIZER_PATTERN = re.compile(
    r'(?P<localizer>\b(?:localizer|[A-Za-z_][A-Za-z0-9_]*localizer[A-Za-z0-9_]*))'
    r'(?P<spacing>\s*)\[\s*"(?P<key>[A-Z][A-Z0-9_]*)"\s*\]',
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Finding:
    """Mô tả một raw localization key được tìm thấy trong mã nguồn C#."""

    service: str
    path: Path
    line: int
    key: str
    identifier: str | None


def configure_output() -> None:
    """Bảo đảm ký tự tiếng Việt được hiển thị đúng trên Windows terminal."""

    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")


def parse_arguments() -> argparse.Namespace:
    """Đọc tham số dòng lệnh của công cụ."""

    default_root = Path(__file__).resolve().parents[4]
    parser = argparse.ArgumentParser(
        description="Rà soát raw IStringLocalizer key và gợi ý LocalizationKeys tương ứng."
    )
    parser.add_argument("--root", type=Path, default=default_root, help="Thư mục gốc BridgeChat.")
    parser.add_argument(
        "--services",
        nargs="+",
        choices=DEFAULT_SERVICES,
        default=list(DEFAULT_SERVICES),
        help="Các service cần rà soát.",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Tự thay raw key bằng LocalizationKeys và thêm using còn thiếu.",
    )
    return parser.parse_args()


def load_localization_keys(root: Path) -> dict[str, str]:
    """Đọc và xác nhận ba tệp tài nguyên có cùng tập key."""

    resources_directory = root / "BridgeChat.SharedLibraries" / "Core.Localization" / "Resources"
    resources: dict[str, dict[str, str]] = {}

    for culture in SUPPORTED_CULTURES:
        resource_path = resources_directory / f"{culture}.json"
        with resource_path.open("r", encoding="utf-8-sig") as resource_file:
            resources[culture] = json.load(resource_file)

    reference_keys = set(resources["en-US"])
    for culture in SUPPORTED_CULTURES[1:]:
        culture_keys = set(resources[culture])
        missing = sorted(reference_keys - culture_keys)
        extra = sorted(culture_keys - reference_keys)
        if missing or extra:
            raise ValueError(
                f"Locale {culture} không đồng bộ; thiếu={missing}, thừa={extra}."
            )

    identifiers = {key: to_identifier(key) for key in sorted(reference_keys)}
    grouped: dict[str, list[str]] = {}
    for key, identifier in identifiers.items():
        grouped.setdefault(identifier, []).append(key)

    collisions = {name: keys for name, keys in grouped.items() if len(keys) > 1}
    if collisions:
        raise ValueError(f"Các localization key tạo trùng định danh C#: {collisions}")

    return identifiers


def to_identifier(key: str) -> str:
    """Chuyển key chữ hoa gạch dưới thành định danh PascalCase giống generator C#."""

    parts = [part for part in re.split(r"[^A-Za-z0-9]+", key) if part]
    identifier = "".join(part[0].upper() + part[1:].lower() for part in parts)
    return f"Key{identifier}" if identifier and identifier[0].isdigit() else identifier


def iter_csharp_files(service_directory: Path):
    """Liệt kê file C# và bỏ qua thư mục build, migration hoặc metadata."""

    for current_root, directories, files in os.walk(service_directory):
        directories[:] = [name for name in directories if name not in EXCLUDED_DIRECTORIES]
        for file_name in files:
            if file_name.endswith(".cs"):
                yield Path(current_root) / file_name


def scan_file(
    service: str,
    source_path: Path,
    identifiers: dict[str, str],
) -> list[Finding]:
    """Tìm raw localization key trong một file C#."""

    source = source_path.read_text(encoding="utf-8-sig")
    findings: list[Finding] = []
    for match in LOCALIZER_PATTERN.finditer(source):
        key = match.group("key")
        line = source.count("\n", 0, match.start()) + 1
        findings.append(Finding(service, source_path, line, key, identifiers.get(key)))
    return findings


def add_localization_using(source: str) -> str:
    """Thêm namespace LocalizationKeys vào vùng using nếu file chưa khai báo."""

    using_statement = f"using {LOCALIZATION_NAMESPACE};"
    if using_statement in source or f"namespace {LOCALIZATION_NAMESPACE}" in source:
        return source

    using_matches = list(re.finditer(r"^using\s+[^;]+;\s*$", source, re.MULTILINE))
    if using_matches:
        insertion = using_matches[-1].end()
        return source[:insertion] + "\n" + using_statement + source[insertion:]

    return using_statement + "\n\n" + source


def fix_file(source_path: Path, identifiers: dict[str, str]) -> int:
    """Thay raw key hợp lệ và duy trì UTF-8 không BOM cùng CRLF."""

    source = source_path.read_text(encoding="utf-8-sig")
    replacement_count = 0

    def replace_match(match: re.Match[str]) -> str:
        nonlocal replacement_count
        identifier = identifiers.get(match.group("key"))
        if identifier is None:
            return match.group(0)
        replacement_count += 1
        return f"{match.group('localizer')}{match.group('spacing')}[LocalizationKeys.{identifier}]"

    updated_source = LOCALIZER_PATTERN.sub(replace_match, source)
    if replacement_count == 0:
        return 0

    updated_source = add_localization_using(updated_source)
    normalized_source = updated_source.replace("\r\n", "\n").replace("\r", "\n").replace("\n", "\r\n")
    source_path.write_text(normalized_source, encoding="utf-8", newline="")
    return replacement_count


def print_report(root: Path, findings: list[Finding], fixed_count: int) -> None:
    """In báo cáo chi tiết và tổng hợp theo service."""

    print("=" * 88)
    print("AUDIT LOCALIZATION KEYS — BRIDGECHAT")
    print("=" * 88)

    for finding in findings:
        relative_path = finding.path.relative_to(root)
        replacement = (
            f"LocalizationKeys.{finding.identifier}"
            if finding.identifier
            else "KEY KHÔNG TỒN TẠI TRONG RESOURCES"
        )
        print(f"{relative_path}:{finding.line}: {finding.key} -> {replacement}")

    print("-" * 88)
    for service in DEFAULT_SERVICES:
        service_findings = [finding for finding in findings if finding.service == service]
        unknown_count = sum(finding.identifier is None for finding in service_findings)
        print(f"{service:<38} raw={len(service_findings):>4} unknown={unknown_count:>3}")

    print("-" * 88)
    print(f"Tổng raw key: {len(findings)}")
    print(f"Key không tồn tại: {sum(finding.identifier is None for finding in findings)}")
    if fixed_count:
        print(f"Đã chuyển đổi: {fixed_count}")


def main() -> int:
    """Điều phối quá trình audit hoặc tự động chuyển đổi."""

    configure_output()
    arguments = parse_arguments()
    root = arguments.root.resolve()

    try:
        identifiers = load_localization_keys(root)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Không thể tải localization resources: {error}", file=sys.stderr)
        return 2

    findings: list[Finding] = []
    for service in arguments.services:
        service_directory = root / service
        if not service_directory.is_dir():
            print(f"Không tìm thấy service: {service_directory}", file=sys.stderr)
            return 2
        for source_path in iter_csharp_files(service_directory):
            findings.extend(scan_file(service, source_path, identifiers))

    fixed_count = 0
    if arguments.fix:
        files_to_fix = {finding.path for finding in findings if finding.identifier is not None}
        fixed_count = sum(fix_file(source_path, identifiers) for source_path in files_to_fix)

    print_report(root, findings, fixed_count)
    has_unknown_keys = any(finding.identifier is None for finding in findings)
    has_unfixed_keys = bool(findings) and not arguments.fix
    return 1 if has_unknown_keys or has_unfixed_keys else 0


if __name__ == "__main__":
    raise SystemExit(main())
