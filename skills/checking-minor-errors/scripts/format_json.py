import json
import os
import sys

# Force UTF-8 stdout
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def format_json_file(filepath, indent=2):
    try:
        with open(filepath, 'rb') as f:
            raw = f.read()

        if not raw.strip():
            return False, "File empty"

        # Decode UTF-8 (strip BOM if any)
        text = raw.decode('utf-8-sig')
        data = json.loads(text)

        # Standard clean formatting with 2 spaces indent and trailing newline
        formatted = json.dumps(data, indent=indent, ensure_ascii=False)
        
        # Enforce CRLF
        lines = formatted.splitlines()
        crlf_content = '\r\n'.join(lines) + '\r\n'

        utf8_bytes = crlf_content.encode('utf-8')
        if utf8_bytes != raw:
            with open(filepath, 'wb') as f:
                f.write(utf8_bytes)
            return True, "Formatted successfully"
        return False, "Already clean"
    except Exception as e:
        return False, f"Error: {e}"

def scan_and_format_json(directory):
    print(f"===========================================================")
    print(f"  FORMATTING & STANDARDIZING ALL JSON FILES IN: {directory}")
    print(f"===========================================================")
    
    total_json = 0
    formatted_count = 0
    error_count = 0

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d.lower() not in ('bin', 'obj', '.git', '.vs', '.agents', '.idea', 'migrations', 'node_modules', 'storagebridgechat', 'dist', 'build', '.gemini')]
        for file in files:
            if file.endswith('.json'):
                total_json += 1
                filepath = os.path.join(root, file)
                changed, msg = format_json_file(filepath, indent=2)
                if changed:
                    formatted_count += 1
                    print(f" [FORMATTED] {filepath}")
                elif "Error" in msg:
                    error_count += 1
                    print(f" [ERROR] {filepath} -> {msg}")

    print(f"\n-----------------------------------------------------------")
    print(f"Total JSON files checked: {total_json}")
    print(f"Total files formatted: {formatted_count}")
    print(f"Total syntax errors: {error_count}")
    print(f"-----------------------------------------------------------")

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else 'E:\\BridgeChat'
    scan_and_format_json(target)
