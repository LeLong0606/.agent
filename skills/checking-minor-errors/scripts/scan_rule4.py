import os
import re
import sys

def scan_rule4(directory):
    violations = []
    for root, dirs, files in os.walk(directory):
        if 'bin' in root or 'obj' in root: continue
        for file in files:
            if not file.endswith('.cs'): continue
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Regex to detect fully qualified name usage inside methods, very basic heuristic
            # We look for "BridgeChat." not preceded by "using " or "namespace "
            for i, line in enumerate(content.splitlines()):
                if 'BridgeChat.' in line and not line.strip().startswith('using ') and not line.strip().startswith('namespace '):
                    # Exclude summary tags
                    if not line.strip().startswith('///'):
                        violations.append(f"{filepath}:{i+1}: Rule 4 Violation - Possible fully qualified name usage ({line.strip()})")
    return violations

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else '.'
    viols = scan_rule4(target)
    for v in viols: print(v)
    if not viols: print("Rule 4: OK")
