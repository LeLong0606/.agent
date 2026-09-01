import os
import re

files = [
    'E:\\BridgeChat\\BridgeChat.GroupService\\BridgeChat.GroupService.Infrastructure\\DependencyInjection.cs',
    'E:\\BridgeChat\\BridgeChat.IdentityService\\BridgeChat.IdentityService.Infrastructure\\DependencyInjection.cs',
    'E:\\BridgeChat\\BridgeChat.UserService\\BridgeChat.UserService.Infrastructure\\DependencyInjection.cs'
]

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    new_content = re.sub(
        r'throw new InvalidOperationException\("Không tìm thấy chuỗi kết nối \'DefaultConnection\' trong cấu hình\."\);',
        r'throw new InvalidOperationException($"Connection string \'DefaultConnection\' not found in configuration.");',
        content
    )
    
    with open(file, 'w', encoding='utf-8', newline='') as f:
        # keep original CRLF
        f.write(new_content)
        
    print(f'Fixed {file}')
