import os
import re
import sys

def scan_rule1(directory):
    violations = []
    for root, dirs, files in os.walk(directory):
        if 'bin' in root or 'obj' in root: continue
        is_application_layer = 'Application' in root.split(os.sep)
        for file in files:
            if not file.endswith('.cs'): continue
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if is_application_layer:
                if re.search(r'using\s+Dapper;', content):
                    violations.append(f"{filepath}: Rule 1 Violation - Dapper is not allowed in Application layer.")
                if re.search(r'IDbConnection', content):
                    violations.append(f"{filepath}: Rule 1 Violation - IDbConnection is not allowed in Application layer.")
                if re.search(r'using\s+Microsoft.EntityFrameworkCore;', content):
                    violations.append(f"{filepath}: Rule 1 Violation - EF Core is forbidden for data access.")
    return violations

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else '.'
    viols = scan_rule1(target)
    for v in viols: print(v)
    if not viols: print("Rule 1: OK")
