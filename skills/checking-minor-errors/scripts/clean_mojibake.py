#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script quét và khôi phục lỗi mã hóa ký tự và lỗi văn bản tiếng Việt bị lỗi thời / biến dạng
(Mojibake, Double-encoded UTF-8, VIQR / Lossy ASCII mangled text) 
trong các file mã nguồn (chủ yếu là .cs) cho dự án BridgeChat.

Đặc trị các lỗi như:
  // 4. XÃ³a OTP khá»i Redis sau khi dÃ¹ng thÃ nh cÃ´ng
  -> // 4. Xóa OTP khỏi Redis sau khi dùng thành công

  /// Lu tr_ khA3a cA'ng khai (IdentityKey, SignedPreKey) cho mTt phiAn/thit b< `ng nh-p.
  -> /// Lưu trữ khóa công khai (IdentityKey, SignedPreKey) cho một phiên/thiết bị đăng nhập.

  /// Ly danh sAch cAc khA3a cA'ng khai `ang hot `Tng c a mTt ng?i dA1ng mc tiAu.
  -> /// Lấy danh sách các khóa công khai đang hoạt động của một người dùng mục tiêu.

Tuân thủ Rule 4 (AGENTS.md):
- Chuẩn hóa Encoding: UTF-8 (không BOM)
- Chuẩn hóa Line Endings: CRLF (\r\n)
"""

import os
import sys
import re
import argparse

# Thiết lập UTF-8 cho console output trên Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Bảng tra cứu các ký tự Windows-1252 (0x80 - 0x9F) về giá trị byte tương ứng
CP1252_MAP = {
    '\u20ac': 0x80, '\u201a': 0x82, '\u0192': 0x83, '\u201e': 0x84,
    '\u2026': 0x85, '\u2020': 0x86, '\u2021': 0x87, '\u02c6': 0x88,
    '\u2030': 0x89, '\u0160': 0x8a, '\u2039': 0x8b, '\u0152': 0x8c,
    '\u017d': 0x8e, '\u2018': 0x91, '\u2019': 0x92, '\u201c': 0x93,
    '\u201d': 0x94, '\u2022': 0x95, '\u2013': 0x96, '\u2014': 0x97,
    '\u02dc': 0x98, '\u2122': 0x99, '\u0161': 0x9a, '\u203a': 0x9b,
    '\u0153': 0x9c, '\u017e': 0x9e, '\u0178': 0x9f,
    # Các mã điều khiển ISO-8859-1 tương ứng
    '\x80': 0x80, '\x81': 0x81, '\x82': 0x82, '\x83': 0x83, '\x84': 0x84,
    '\x85': 0x85, '\x86': 0x86, '\x87': 0x87, '\x88': 0x88, '\x89': 0x89,
    '\x8a': 0x8a, '\x8b': 0x8b, '\x8c': 0x8c, '\x8d': 0x8d, '\x8e': 0x8e,
    '\x8f': 0x8f, '\x90': 0x90, '\x91': 0x91, '\x92': 0x92, '\x93': 0x93,
    '\x94': 0x94, '\x95': 0x95, '\x96': 0x96, '\x97': 0x97, '\x98': 0x98,
    '\x99': 0x99, '\x9a': 0x9a, '\x9b': 0x9b, '\x9c': 0x9c, '\x9d': 0x9d,
    '\x9e': 0x9e, '\x9f': 0x9f,
}

# Regex nhận diện các cụm byte bị double-encode toàn diện cho tiếng Việt
MOJIBAKE_CLUSTER_PATTERN = re.compile(
    r'(?:[\u00C2-\u00DF\u00E0-\u00EF][\u0080-\u00FF\u0100-\u02C6\u2000-\u2122]{1,3})+'
)

# Danh mục thay thế các mẫu chuỗi lỗi ASCII/VIQR/Mangled bị mất dấu
MANGLED_TEXT_REPLACEMENTS = [
    (
        r'Lu\s*tr_\s*khA3a\s*cA\'?ng\s*khai\s*\(IdentityKey,\s*SignedPreKey\)\s*cho\s*mTt\s*phiAn/thit\s*b<\s*`?ng\s*nh-p\.?',
        'Lưu trữ khóa công khai (IdentityKey, SignedPreKey) cho một phiên/thiết bị đăng nhập.'
    ),
    (
        r'Ly\s*danh\s*sAch\s*cAc\s*khA3a\s*cA\'?ng\s*khai\s*`?ang\s*hot\s*`?Tng\s*c\s*a\s*mTt\s*ng\?i\s*dA1ng\s*mc\s*tiAu\.?',
        'Lấy danh sách các khóa công khai đang hoạt động của một người dùng mục tiêu.'
    ),
    (r'\bkhA3a\s*cA\'?ng\s*khai\b', 'khóa công khai'),
    (r'\bLy\s*danh\s*sAch\b', 'Lấy danh sách'),
    (r'\bcAc\s*khA3a\b', 'các khóa'),
    (r'\b`?ang\s*hot\s*`?Tng\b', 'đang hoạt động'),
    (r'\bc\s*a\s*mTt\s*ng\?i\s*dA1ng\b', 'của một người dùng'),
    (r'\bmc\s*tiAu\b', 'mục tiêu'),
    (r'\bmTt\s*phiAn/thit\s*b<\b', 'một phiên/thiết bị'),
    (r'\b`?ng\s*nh-p\b', 'đăng nhập'),
    (r'\bLu\s*tr_\b', 'Lưu trữ'),
]

IGNORED_DIRS = {
    'bin', 'obj', '.git', '.vs', '.agents', '.idea', 
    'node_modules', 'storagebridgechat', 'dist', 'build'
}

def to_byte(char: str):
    """Chuyển đổi ký tự unicode đơn về mã byte tương ứng theo CP1252 / Latin-1."""
    if char in CP1252_MAP:
        return CP1252_MAP[char]
    code = ord(char)
    if 0x00 <= code <= 0xFF:
        return code
    return None

def decode_mojibake_bytes(segment: str) -> str:
    """Khôi phục một phân đoạn chuỗi byte bị lỗi mã hóa UTF-8 kép."""
    byte_list = []
    for c in segment:
        b = to_byte(c)
        if b is None:
            return segment
        byte_list.append(b)
    
    # 1. Thử giải mã toàn bộ cụm byte sang UTF-8
    try:
        return bytes(byte_list).decode('utf-8')
    except Exception:
        pass
    
    # 2. Nếu toàn bộ cụm không khớp, quét tiền tố UTF-8 hợp lệ
    res = ''
    idx = 0
    while idx < len(byte_list):
        matched = False
        for length in (4, 3, 2, 1):
            if idx + length <= len(byte_list):
                try:
                    chunk = bytes(byte_list[idx:idx+length]).decode('utf-8')
                    res += chunk
                    idx += length
                    matched = True
                    break
                except Exception:
                    pass
        if not matched:
            res += segment[idx]
            idx += 1
    return res

def fix_mangled_ascii(text: str) -> str:
    """Khôi phục các chuỗi lỗi mã hóa ASCII/VIQR/Mangled."""
    for pattern, repl in MANGLED_TEXT_REPLACEMENTS:
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
    return text

def fix_mojibake_in_text(text: str) -> str:
    """Quét và sửa toàn bộ lỗi mojibake và mangled text trong văn bản."""
    # 1. Khôi phục mangled ASCII text
    text = fix_mangled_ascii(text)
    
    # 2. Khôi phục double-encoded UTF-8 qua nhiều tầng
    def _replace_callback(match):
        seg = match.group(0)
        return decode_mojibake_bytes(seg)
    
    current = text
    for _ in range(5):
        fixed = MOJIBAKE_CLUSTER_PATTERN.sub(_replace_callback, current)
        if fixed == current:
            break
        current = fixed
    return current

def process_file(filepath: str, dry_run: bool = False) -> tuple[bool, list[tuple[int, str, str]]]:
    """
    Xử lý một file: Đọc, phát hiện và sửa mojibake/mangled text, đảm bảo EOL là CRLF.
    Trả về (is_modified, list_of_changes).
    """
    try:
        with open(filepath, 'rb') as f:
            raw_bytes = f.read()
    except Exception as e:
        print(f"[!] Không thể đọc file {filepath}: {e}")
        return False, []
    
    # Bỏ BOM nếu có để đảm bảo UTF-8 without BOM
    if raw_bytes.startswith(b'\xef\xbb\xbf'):
        raw_bytes = raw_bytes[3:]
    
    try:
        content = raw_bytes.decode('utf-8')
    except UnicodeDecodeError:
        content = raw_bytes.decode('utf-8', errors='replace')
    
    lines = content.splitlines()
    modified_lines = []
    new_lines = []
    
    for line_idx, line in enumerate(lines, start=1):
        fixed_line = fix_mojibake_in_text(line)
        if fixed_line != line:
            modified_lines.append((line_idx, line, fixed_line))
        new_lines.append(fixed_line)
    
    # Chuẩn hóa CRLF và UTF-8
    new_content = '\r\n'.join(new_lines)
    if new_lines:
        new_content += '\r\n'
    
    new_bytes = new_content.encode('utf-8')
    is_modified = (new_bytes != raw_bytes)
    
    if is_modified and not dry_run:
        with open(filepath, 'wb') as f:
            f.write(new_bytes)
            
    return is_modified, modified_lines

def scan_and_fix(target_dir: str, extensions: list[str], dry_run: bool = False):
    """Duyệt qua cây thư mục và xử lý các file khớp phần mở rộng."""
    print(f"{'='*70}")
    print(f"🚀 BẮT ĐẦU QUÉT VÀ SỬA MOJIBAKE TRONG THƯ MỤC: {target_dir}")
    print(f"   - Các đuôi file: {', '.join(extensions)}")
    print(f"   - Chế độ: {'DRY RUN (Chỉ kiểm tra)' if dry_run else 'APPLY FIX (Sửa trực tiếp)'}")
    print(f"{'='*70}\n")
    
    total_files_scanned = 0
    files_with_issues = 0
    total_lines_fixed = 0
    
    for root, dirs, files in os.walk(target_dir):
        # Bỏ qua các thư mục không cần thiết
        dirs[:] = [d for d in dirs if d.lower() not in IGNORED_DIRS]
        
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in extensions:
                total_files_scanned += 1
                filepath = os.path.join(root, file)
                is_mod, changes = process_file(filepath, dry_run=dry_run)
                
                if changes or is_mod:
                    files_with_issues += 1
                    total_lines_fixed += len(changes)
                    rel_path = os.path.relpath(filepath, target_dir)
                    
                    status_tag = "[DRY-RUN]" if dry_run else "[FIXED]"
                    print(f"{status_tag} {rel_path} ({len(changes)} dòng bị lỗi)")
                    
                    for line_num, orig, fixed in changes[:5]: # In tối đa 5 dòng mẫu
                        print(f"   Line {line_num:4d} | GỐC: {orig.strip()}")
                        print(f"             | SỬA: {fixed.strip()}")
                    if len(changes) > 5:
                        print(f"             | ... và {len(changes) - 5} dòng khác.")
                    print("-" * 70)

    print("\n" + "="*70)
    print("📊 TỔNG KẾT BÁO CÁO:")
    print(f"   - Tổng số file đã quét: {total_files_scanned}")
    print(f"   - Số file có lỗi phát hiện & khôi phục: {files_with_issues}")
    print(f"   - Tổng số dòng đã được khôi phục: {total_lines_fixed}")
    print(f"   - Trạng thái: {'HOÀN TẤT' if not dry_run else 'KIỂM TRA XONG (Chưa ghi đè file)'}")
    print("="*70)

def main():
    parser = argparse.ArgumentParser(
        description="Quét và sửa lỗi mã hóa tiếng Việt (Mojibake / Double UTF-8 / VIQR) cho BridgeChat."
    )
    parser.add_argument(
        "target_dir", 
        nargs="?", 
        default=os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")),
        help="Đường dẫn thư mục cần quét (mặc định là root của BridgeChat)"
    )
    parser.add_argument(
        "--ext", 
        nargs="+", 
        default=[".cs", ".csproj", ".props", ".targets", ".xml", ".json", ".md"],
        help="Danh sách phần mở rộng cần quét (mặc định: .cs, .csproj, .props, .targets, .xml, .json, .md)"
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        help="Chỉ kiểm tra và in danh sách dòng lỗi, không ghi đè file"
    )
    
    args = parser.parse_args()
    target_path = os.path.abspath(args.target_dir)
    
    if not os.path.exists(target_path):
        print(f"[X] Đường dẫn không tồn tại: {target_path}")
        sys.exit(1)
        
    scan_and_fix(target_path, [e if e.startswith('.') else f'.{e}' for e in args.ext], dry_run=args.dry_run)

if __name__ == "__main__":
    main()
