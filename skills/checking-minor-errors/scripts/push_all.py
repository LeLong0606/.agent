#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tự động duyệt qua tất cả các Microservices, SharedLibraries và Frontend trong BridgeChat
để kiểm tra trạng thái Git, tự động Commit và Push lên GitHub.

Các tính năng:
- Hỗ trợ commit message tùy biến (--message / -m).
- Tự động thử lại (Retry) khi gặp sự cố mạng hoặc timeout kết nối GitHub.
- Hỗ trợ chế độ chỉ kiểm tra trạng thái (--status / -s).
- Hỗ trợ chỉ định branch đích (--branch / -b, mặc định: master).
"""

import os
import sys
import subprocess
import time
import argparse

# Thiết lập UTF-8 cho console output trên Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SERVICES = [
    "BridgeChat.APIGateway",
    "BridgeChat.AttachmentService",
    "BridgeChat.ConnectionService",
    "BridgeChat.GroupService",
    "BridgeChat.IdentityService",
    "BridgeChat.MessageService",
    "BridgeChat.NotificationService",
    "BridgeChat.PresenceService",
    "BridgeChat.SearchService",
    "BridgeChat.SharedLibraries",
    "BridgeChat.UserService",
    "bridgechatwebreact"
]

def run_git(cmd: list[str], cwd: str) -> tuple[int, str, str]:
    """Chạy lệnh Git và trả về (returncode, stdout, stderr)."""
    res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    return res.returncode, res.stdout.strip(), res.stderr.strip()

def process_repo(root_dir: str, service_name: str, commit_msg: str, branch: str, status_only: bool, max_retries: int = 3):
    service_path = os.path.join(root_dir, service_name)
    
    if not os.path.exists(service_path):
        print(f"[-] {service_name}: Thư mục không tồn tại!")
        return
    
    git_dir = os.path.join(service_path, ".git")
    if not os.path.exists(git_dir):
        print(f"[-] {service_name}: Không phải là Git repository!")
        return
    
    # 1. Kiểm tra trạng thái Git
    _, status_out, _ = run_git(["git", "status", "--porcelain"], service_path)
    _, branch_out, _ = run_git(["git", "branch", "--show-current"], service_path)
    current_branch = branch_out or branch
    
    # Kiểm tra xem có commit nào chưa push không
    _, unpushed_out, _ = run_git(["git", "log", f"origin/{current_branch}..HEAD", "--oneline"], service_path)
    has_uncommitted = bool(status_out)
    has_unpushed = bool(unpushed_out)
    
    if status_only:
        state_str = "CLEAN"
        if has_uncommitted and has_unpushed:
            state_str = f"DIRTY & {len(unpushed_out.splitlines())} UNPUSHED COMMITS"
        elif has_uncommitted:
            state_str = "DIRTY (Chưa commit)"
        elif has_unpushed:
            state_str = f"{len(unpushed_out.splitlines())} UNPUSHED COMMITS"
            
        print(f"📁 {service_name:30s} [{current_branch}]: {state_str}")
        if has_uncommitted:
            for line in status_out.splitlines()[:5]:
                print(f"     {line}")
        return

    # 2. Xử lý commit nếu có thay đổi
    if has_uncommitted:
        print(f"\n⚡ [CHANGES] {service_name}: Tìm thấy thay đổi, đang commit...")
        run_git(["git", "add", "."], service_path)
        code, commit_res, err = run_git(["git", "commit", "-m", commit_msg], service_path)
        if code == 0:
            print(f"   ✓ Commit thành công: {commit_res.splitlines()[0] if commit_res else ''}")
        else:
            print(f"   ✗ Commit thất bại: {err}")
            return
        has_unpushed = True

    # 3. Xử lý push lên GitHub nếu có commit chưa push
    if has_unpushed:
        print(f"🚀 [PUSHING] {service_name} -> origin/{current_branch}...")
        pushed = False
        for attempt in range(1, max_retries + 1):
            code, push_out, push_err = run_git(["git", "push", "origin", current_branch], service_path)
            if code == 0:
                print(f"   ✅ Push thành công {service_name} lên {current_branch}!")
                pushed = True
                break
            else:
                print(f"   ⚠️ Thử lần {attempt}/{max_retries} thất bại: {push_err or push_out}")
                if attempt < max_retries:
                    time.sleep(2)
        if not pushed:
            print(f"   ❌ Không thể push {service_name} sau {max_retries} lần thử!")
    else:
        print(f"✓ {service_name:30s} : Sạch và đã đồng bộ với origin/{current_branch}.")

def main():
    parser = argparse.ArgumentParser(
        description="Script tự động commit và push toàn bộ các service trong BridgeChat."
    )
    parser.add_argument(
        "-m", "--message",
        default="chore: apply architecture optimizations and rule compliance",
        help="Nội dung thông điệp commit (mặc định: 'chore: apply architecture optimizations and rule compliance')"
    )
    parser.add_argument(
        "-b", "--branch",
        default="master",
        help="Tên nhánh cần push (mặc định: master)"
    )
    parser.add_argument(
        "-s", "--status",
        action="store_true",
        help="Chỉ kiểm tra trạng thái của tất cả các repo, không commit hay push"
    )
    parser.add_argument(
        "--path",
        default=os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")),
        help="Đường dẫn thư mục gốc BridgeChat"
    )
    
    args = parser.parse_args()
    root_dir = os.path.abspath(args.path)
    
    print("=" * 70)
    if args.status:
        print("🔍 KIỂM TRA TRẠNG THÁI GIT TOÀN BỘ CÁC SERVICE")
    else:
        print("🚀 BẮT ĐẦU QUY TRÌNH COMMIT & PUSH TOÀN BỘ CÁC SERVICE")
        print(f"   - Commit Message: \"{args.message}\"")
        print(f"   - Target Branch : {args.branch}")
    print("=" * 70)
    
    for service in SERVICES:
        process_repo(root_dir, service, args.message, args.branch, args.status)
        
    print("=" * 70)
    print("✨ Hoàn tất quy trình!")

if __name__ == "__main__":
    main()
