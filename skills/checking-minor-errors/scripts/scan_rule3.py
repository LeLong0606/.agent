import os
import re
import sys

def scan_rule3(directory):
    violations = []
    for root, dirs, files in os.walk(directory):
        if 'bin' in root or 'obj' in root: continue
        for file in files:
            if not file.endswith('.cs'): continue
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if 'Dto' in file and file.endswith('Dto.cs'):
                violations.append(f"{filepath}: Rule 3 Violation - Dto suffix is forbidden.")
                
            if file.endswith('Response.cs'):
                if 'public class' in content and 'Response' in content:
                    violations.append(f"{filepath}: Rule 3 Violation - Responses must be records, not classes.")
            
            if file.endswith('Request.cs'):
                if 'public record' in content and 'Request' in content:
                    violations.append(f"{filepath}: Rule 3 Violation - Request models must be classes, not records.")
                    
            if file.endswith('Validator.cs') and 'AbstractValidator' in content:
                if 'IStringLocalizer<GlobalResource>' not in content:
                    violations.append(f"{filepath}: Rule 3 Violation - Validator must inject IStringLocalizer<GlobalResource>.")
    return violations

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else '.'
    viols = scan_rule3(target)
    for v in viols: print(v)
    if not viols: print("Rule 3: OK")
