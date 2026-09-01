import os
import re

def scan_files(root_dir):
    violations = []
    
    # regex to find _logger.Log...( "..." ) or throw new ...Exception( "..." )
    logger_pattern = re.compile(r'(_logger\.Log(?:Information|Error|Warning|Debug|Trace)\s*\(\s*(?:ex\s*,\s*)?)(?:"|\$")')
    throw_pattern = re.compile(r'(throw\s+new\s+[A-Za-z0-9_]+Exception\s*\(\s*)(?:"|\$")')
    
    for subdir, dirs, files in os.walk(root_dir):
        if 'bin' in subdir or 'obj' in subdir or '.git' in subdir:
            continue
        for file in files:
            if file.endswith('.cs'):
                filepath = os.path.join(subdir, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    try:
                        lines = f.readlines()
                        for i, line in enumerate(lines):
                            if logger_pattern.search(line) or throw_pattern.search(line):
                                violations.append((filepath, i+1, line.strip()))
                    except Exception as e:
                        pass
    return violations

if __name__ == '__main__':
    root_dir = 'E:\\BridgeChat'
    violations = scan_files(root_dir)
    if violations:
        print(f'Found {len(violations)} violations:')
        for v in violations:
            print(f'{v[0]}:{v[1]}: {v[2]}')
    else:
        print('No violations found!')

