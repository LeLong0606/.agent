import os
import re
import sys

def scan_rule5(directory):
    violations = []
    for root, dirs, files in os.walk(directory):
        if 'bin' in root or 'obj' in root: continue
        for file in files:
            if not file.endswith('.cs'): continue
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if file == 'Program.cs':
                if 'CultureInfo.DefaultThreadCurrentCulture = new CultureInfo("vi-VN");' not in content:
                    violations.append(f"{filepath}: Rule 5 Violation - Missing vi-VN thread culture setup.")
                
            # Log and Throw hardcoded string checks
            lines = content.splitlines()
            for i, line in enumerate(lines):
                if re.search(r'throw\s+new\s+[A-Za-z0-9_]+Exception\s*\(\s*(?:"|\$")', line):
                    violations.append(f"{filepath}:{i+1}: Rule 5 Violation - Hardcoded string in Exception.")
                if re.search(r'_logger\.Log[A-Za-z]+\s*\(\s*(?:"|\$")', line):
                    violations.append(f"{filepath}:{i+1}: Rule 5 Violation - Hardcoded string in _logger.")
    return violations

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else '.'
    viols = scan_rule5(target)
    for v in viols: print(v)
    if not viols: print("Rule 5: OK")
