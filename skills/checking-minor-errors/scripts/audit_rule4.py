import os
import re
import sys

# Force UTF-8 stdout
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def check_file_rule4(filepath):
    issues = []
    try:
        with open(filepath, 'rb') as f:
            raw = f.read()

        if not raw:
            return issues

        # Check BOM
        if raw.startswith(b'\xef\xbb\xbf'):
            issues.append("Contains UTF-8 BOM (Rule 4 requires pure UTF-8)")

        # Decode
        try:
            text = raw.decode('utf-8')
        except UnicodeDecodeError:
            issues.append("Corrupted Encoding (Cannot decode as UTF-8)")
            return issues

        # Check CRLF
        if '\r\n' not in text and '\n' in text:
            issues.append("Incorrect EOL (Uses LF instead of CRLF)")
        elif '\n' in text and text.count('\n') != text.count('\r\n'):
            issues.append("Mixed EOL (Contains bare LF)")

        # Check comments and documentation rules in C# files
        if filepath.endswith('.cs'):
            lines = text.splitlines()
            for idx, line in enumerate(lines):
                line_num = idx + 1
                stripped = line.strip()

                # Check Forbidden Meta Tags
                if re.search(r'//.*(Giải thích\s*\(Why\)|Cụ thể\s*\(How\))', line, re.IGNORECASE):
                    issues.append(f"Line {line_num}: Forbidden meta comment tag '(Why)' or '(How)'")

                # Check Non-Vietnamese XML comments (English heuristics)
                if stripped.startswith('///'):
                    # Flag common English-only starter words in summary
                    if re.search(r'///\s*<summary>\s*(Initializes|Gets or sets|Represents|Handles|Creates|Processes|Updates|Deletes|Service for|Controller for)\b', line, re.IGNORECASE):
                        issues.append(f"Line {line_num}: English XML doc comment detected (Must be Vietnamese)")

                # Check Fully Qualified Name (FQN) inside method bodies
                if 'BridgeChat.' in line and not stripped.startswith('using ') and not stripped.startswith('namespace ') and not stripped.startswith('//') and not stripped.startswith('///'):
                    # Exclude known strings like assembly names, URLs, constants
                    if not re.search(r'(".*BridgeChat\..*"|typeof\(|MigrationsAssembly)', line):
                        issues.append(f"Line {line_num}: Possible FQN violation ('{stripped}')")

                # Public types must be documented. Previously the audit only
                # validated XML comments that already existed, so an entirely
                # missing <summary> (for example InitialBackupRequest) passed.
                if re.match(
                    r'^public\s+(?:(?:abstract|sealed|static|partial|readonly|ref)\s+)*'
                    r'(?:class|record(?:\s+class|\s+struct)?|struct|interface|enum)\s+\w+',
                    stripped,
                ):
                    previous = idx - 1
                    while previous >= 0 and not lines[previous].strip():
                        previous -= 1

                    # Attributes may sit between XML documentation and the type.
                    while previous >= 0 and lines[previous].strip().startswith('['):
                        previous -= 1
                        while previous >= 0 and not lines[previous].strip():
                            previous -= 1

                    doc_lines = []
                    while previous >= 0 and lines[previous].strip().startswith('///'):
                        doc_lines.append(lines[previous].strip())
                        previous -= 1

                    if not any('<summary>' in doc for doc in doc_lines):
                        issues.append(
                            f"Line {line_num}: Public type is missing Vietnamese XML <summary> documentation"
                        )

    except Exception as e:
        issues.append(f"Error reading file: {e}")

    return issues

def scan_all(directory):
    total_files = 0
    issue_count = 0
    print(f"===========================================================")
    print(f"  FULL RULE 4 AUDIT FOR: {directory}")
    print(f"===========================================================")

    for root, dirs, files in os.walk(directory):
        excluded_dirs = ('bin', 'obj', '.git', '.vs', '.agents', '.idea', 'migrations',
                         'node_modules', 'storagebridgechat', 'dist', 'build', '.gemini')
        dirs[:] = [
            d for d in dirs
            if d.lower() not in excluded_dirs and not d.lower().startswith('.minor-scan-')
        ]
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in ('.cs', '.json', '.md', '.csproj', '.slnx', '.sln'):
                total_files += 1
                filepath = os.path.join(root, file)
                file_issues = check_file_rule4(filepath)
                if file_issues:
                    issue_count += len(file_issues)
                    print(f"\n[VIOLATION] {filepath}")
                    for issue in file_issues:
                        print(f"   -> {issue}")

    print(f"\n-----------------------------------------------------------")
    print(f"Total files checked: {total_files}")
    print(f"Total Rule 4 issues: {issue_count}")
    if issue_count == 0:
        print("RESULT: 100% COMPLIANT WITH RULE 4!")
    print(f"-----------------------------------------------------------")

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else 'E:\\BridgeChat'
    scan_all(target)
