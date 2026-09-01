import os
import re
import sys

def scan_rule2(directory):
    violations = []
    for root, dirs, files in os.walk(directory):
        if 'bin' in root or 'obj' in root: continue
        for file in files:
            if not file.endswith('Controller.cs'): continue
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if re.search(r'\[FromQuery\]|\[FromRoute\]', content):
                violations.append(f"{filepath}: Rule 2 Violation - Input data must not be passed via URL.")
                
            if re.search(r'\[Route\("api/\[controller\]"\)\]', content):
                violations.append(f"{filepath}: Rule 2 Violation - [controller] macro is forbidden in routing.")
    return violations

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else '.'
    viols = scan_rule2(target)
    for v in viols: print(v)
    if not viols: print("Rule 2: OK")
