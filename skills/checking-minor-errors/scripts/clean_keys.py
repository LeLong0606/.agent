import json
import os

files = [
    r"E:\BridgeChat\BridgeChat.SharedLibraries\Core.Localization\Resources\en-US.json",
    r"E:\BridgeChat\BridgeChat.SharedLibraries\Core.Localization\Resources\vi-VN.json",
    r"E:\BridgeChat\BridgeChat.SharedLibraries\Core.Localization\Resources\zh-CN.json"
]

keys_to_remove = [
    "MessageNotFound",
    "NotMessageOwner",
    "MessageIdRequired",
    "MessageContentRequired",
    "MessageContentTooLong",
    "EmojiRequired",
    "EmojiTooLong"
]

for file_path in files:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        modified = False
        for key in keys_to_remove:
            if key in data:
                del data[key]
                modified = True
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                f.write("\n")
            print(f"Cleaned {os.path.basename(file_path)}")
    else:
        print(f"File not found: {file_path}")
