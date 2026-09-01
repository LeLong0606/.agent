import os
import sys

replacements = {
    '"MessageNotFound"': '"MESSAGE_NOT_FOUND"',
    '"NotMessageOwner"': '"NOT_MESSAGE_OWNER"',
    '"MessageIdRequired"': '"MESSAGE_ID_REQUIRED"',
    '"MessageContentRequired"': '"MESSAGE_CONTENT_REQUIRED"',
    '"MessageContentTooLong"': '"MESSAGE_CONTENT_TOO_LONG"',
    '"EmojiRequired"': '"EMOJI_REQUIRED"',
    '"EmojiTooLong"': '"EMOJI_TOO_LONG"'
}

def replace_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content
        for old_val, new_val in replacements.items():
            new_content = new_content.replace(old_val, new_val)
            
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                f.write(new_content)
            print(f"Updated {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def process_directory(directory, ext_filter):
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d.lower() not in ('bin', 'obj', '.git', '.vs')]
        for file in files:
            if file.endswith(ext_filter):
                replace_in_file(os.path.join(root, file))

if __name__ == '__main__':
    # Fix JSON files
    replace_in_file(r'E:\BridgeChat\BridgeChat.SharedLibraries\Core.Localization\Resources\en-US.json')
    replace_in_file(r'E:\BridgeChat\BridgeChat.SharedLibraries\Core.Localization\Resources\vi-VN.json')
    replace_in_file(r'E:\BridgeChat\BridgeChat.SharedLibraries\Core.Localization\Resources\zh-CN.json')
    
    # Fix C# files in MessageService
    process_directory(r'E:\BridgeChat\BridgeChat.MessageService', '.cs')
    print("Done replacing keys!")
