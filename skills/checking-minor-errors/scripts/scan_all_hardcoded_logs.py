import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def scan_hardcoded_logs(directory):
    violations = []
    for root, dirs, files in os.walk(directory):
        if 'bin' in root or 'obj' in root or 'bridgechatwebreact' in root or '.git' in root or '.agents' in root or 'Migrations' in root:
            continue
        for file in files:
            if not file.endswith('.cs'):
                continue
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
            except Exception as e:
                continue

            for i, line in enumerate(lines):
                # 1. Any Logging call (.LogInformation, .LogWarning, .LogError, .LogDebug, .LogTrace, .LogCritical) with quote
                if re.search(r'\.Log(?:Information|Warning|Error|Debug|Trace|Critical)\s*\(', line) and ('"' in line or '$"' in line):
                    if '_localizer' not in line and 'Resource' not in line:
                        violations.append(f"{filepath}:{i+1}: Hardcoded Log -> {line.strip()}")
                
                # 2. Exception throws
                if 'throw new ' in line and ('"' in line or '$"' in line):
                    if '_localizer' not in line and 'Resource' not in line:
                        violations.append(f"{filepath}:{i+1}: Hardcoded Exception -> {line.strip()}")

                # 3. Console.Write/WriteLine
                if 'Console.Write' in line:
                    violations.append(f"{filepath}:{i+1}: Hardcoded Console -> {line.strip()}")

    return violations

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else '.'
    viols = scan_hardcoded_logs(target)
    for v in viols:
        print(v)
    print(f"Total violations found: {len(viols)}")
