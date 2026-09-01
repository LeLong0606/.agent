import os
import sys

def process_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            raw = f.read()

        if not raw:
            return

        # Decode content safely
        if raw.startswith(b'\xef\xbb\xbf'):
            text = raw.decode('utf-8-sig') # Strip BOM
        else:
            try:
                text = raw.decode('utf-8')
            except UnicodeDecodeError:
                # Fallback if somehow it was saved as windows-1252
                text = raw.decode('windows-1252')
        
        # Enforce CRLF
        lines = text.splitlines()
        new_text = '\r\n'.join(lines)
        
        # Preserve trailing newline if it existed
        if text.endswith('\n') or text.endswith('\r'):
            new_text += '\r\n'

        # Encode back to pure UTF-8 (NO BOM)
        new_bytes = new_text.encode('utf-8')
        
        # Only rewrite if there is a change (avoid unnecessary disk I/O)
        if raw != new_bytes:
            with open(filepath, 'wb') as f:
                f.write(new_bytes)
            print(f"Fixed formatting: {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def process_directory(directory):
    valid_exts = {'.cs', '.json', '.md', '.csproj', '.slnx', '.sln'}
    for root, dirs, files in os.walk(directory):
        # Exclude build and version control folders
        dirs[:] = [d for d in dirs if d.lower() not in ('bin', 'obj', '.git', '.vs', '.agents', '.idea')]
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in valid_exts:
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python format_encoding_eol.py <directory>")
        sys.exit(1)
    
    target_dir = sys.argv[1]
    if not os.path.isdir(target_dir):
        print(f"Directory not found: {target_dir}")
        sys.exit(1)
        
    print(f"Scanning and formatting '{target_dir}' to strict UTF-8 (No BOM) and CRLF...")
    process_directory(target_dir)
    print("Done!")
