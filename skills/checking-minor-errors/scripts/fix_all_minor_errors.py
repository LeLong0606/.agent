import os
import json
import re

# 1. Bổ sung các key tài nguyên đa ngôn ngữ vào 3 file JSON
res_dir = 'E:\\BridgeChat\\BridgeChat.SharedLibraries\\Core.Localization\\Resources'
new_keys = {
    'LOG_CONN_MSG_CREATED_RECEIVED': {
        'en-US': 'MessageCreatedEventConsumer received message. ParticipantIds count: {0}, TargetUserId: {1}',
        'vi-VN': 'MessageCreatedEventConsumer nhận được tin nhắn. Số lượng người tham gia: {0}, TargetUserId: {1}',
        'zh-CN': 'MessageCreatedEventConsumer 收到消息。参与者数量: {0}, TargetUserId: {1}'
    },
    'LOG_NOTIF_MSG_CREATED_RECEIVED': {
        'en-US': 'Received new message from Message Queue. Preparing to send Notification via SignalR.',
        'vi-VN': 'Nhận được tin nhắn mới từ Message Queue. Chuẩn bị bắn Notification qua SignalR.',
        'zh-CN': '从消息队列收到新消息。准备通过 SignalR 发送通知。'
    },
    'VAL_USER_ID_REQUIRED': {
        'en-US': 'User ID is required.',
        'vi-VN': 'ID người dùng là bắt buộc.',
        'zh-CN': '用户 ID 必填。'
    },
    'VAL_BLOCKER_ID_REQUIRED': {
        'en-US': 'Blocker ID is required.',
        'vi-VN': 'ID người chặn là bắt buộc.',
        'zh-CN': '阻止者 ID 必填。'
    },
    'VAL_BLOCKED_ID_REQUIRED': {
        'en-US': 'Blocked ID is required.',
        'vi-VN': 'ID người bị chặn là bắt buộc.',
        'zh-CN': '被阻止者 ID 必填。'
    },
    'VAL_CONTACT_ID_REQUIRED': {
        'en-US': 'Contact ID is required.',
        'vi-VN': 'ID danh bạ là bắt buộc.',
        'zh-CN': '联系人 ID 必填。'
    },
    'VAL_USERNAME_REQUIRED': {
        'en-US': 'Username is required.',
        'vi-VN': 'Tên đăng nhập là bắt buộc.',
        'zh-CN': '用户名必填。'
    },
    'VAL_SETTING_ID_REQUIRED': {
        'en-US': 'Setting ID is required.',
        'vi-VN': 'ID cài đặt là bắt buộc.',
        'zh-CN': '设置 ID 必填。'
    }
}

for lang in ['en-US', 'vi-VN', 'zh-CN']:
    filepath = os.path.join(res_dir, f"{lang}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        changed = False
        for k, v in new_keys.items():
            if k not in data:
                data[k] = v[lang]
                changed = True
        
        if changed:
            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                json_str = json.dumps(data, ensure_ascii=False, indent=2)
                f.write(json_str + '\r\n')
            print(f"Updated localization resources: {lang}.json")

# 2. Sửa lỗi Rule 5 tại ConnectionService MessageCreatedEventConsumer.cs
conn_consumer_path = 'E:\\BridgeChat\\BridgeChat.ConnectionService\\BridgeChat.ConnectionService.Infrastructure\\Consumers\\MessageCreatedEventConsumer.cs'
if os.path.exists(conn_consumer_path):
    with open(conn_consumer_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    old_log = '_logger.LogInformation("MessageCreatedEventConsumer received message. ParticipantIds count: {Count}, TargetUserId: {TargetUserId}", \n            message.ParticipantIds?.Count ?? 0, message.TargetUserId);'
    new_log = '_logger.LogInformation(_localizer["LOG_CONN_MSG_CREATED_RECEIVED"].Value, \n            message.ParticipantIds?.Count ?? 0, message.TargetUserId);'
    
    if old_log in content:
        content = content.replace(old_log, new_log)
        with open(conn_consumer_path, 'w', encoding='utf-8', newline='') as f:
            f.write(content)
        print("Fixed Rule 5 in MessageCreatedEventConsumer.cs")
    else:
        # Retry with simpler regex or string match if whitespace differed
        content = re.sub(
            r'_logger\.LogInformation\("MessageCreatedEventConsumer received message[^"]+",\s*message\.ParticipantIds\?\.Count \?\? 0,\s*message\.TargetUserId\);',
            '_logger.LogInformation(_localizer["LOG_CONN_MSG_CREATED_RECEIVED"].Value, message.ParticipantIds?.Count ?? 0, message.TargetUserId);',
            content
        )
        with open(conn_consumer_path, 'w', encoding='utf-8', newline='') as f:
            f.write(content)
        print("Fixed Rule 5 (regex) in MessageCreatedEventConsumer.cs")

# 3. Sửa lỗi Rule 5 tại NotificationService NotificationMessageCreatedEventConsumer.cs
notif_consumer_path = 'E:\\BridgeChat\\BridgeChat.NotificationService\\BridgeChat.NotificationService.Api\\Consumers\\NotificationMessageCreatedEventConsumer.cs'
if os.path.exists(notif_consumer_path):
    with open(notif_consumer_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'IStringLocalizer<GlobalResource>' not in content:
        content = content.replace(
            'private readonly ILogger<NotificationMessageCreatedEventConsumer> _logger;',
            'private readonly ILogger<NotificationMessageCreatedEventConsumer> _logger;\n    private readonly IStringLocalizer<GlobalResource> _localizer;'
        )
        content = content.replace(
            'ILogger<NotificationMessageCreatedEventConsumer> logger)',
            'ILogger<NotificationMessageCreatedEventConsumer> logger,\n        IStringLocalizer<GlobalResource> localizer)'
        )
        content = content.replace(
            '_logger = logger;',
            '_logger = logger;\n        _localizer = localizer;'
        )
    
    content = re.sub(
        r'_logger\.LogInformation\("Nhận được tin nhắn mới từ Message Queue[^"]+"\);',
        '_logger.LogInformation(_localizer["LOG_NOTIF_MSG_CREATED_RECEIVED"].Value);',
        content
    )
    with open(notif_consumer_path, 'w', encoding='utf-8', newline='') as f:
        f.write(content)
    print("Fixed Rule 5 in NotificationMessageCreatedEventConsumer.cs")

# 4. Sửa lỗi Rule 3 tại ApiResponse.cs (chuyển class sang record)
api_res_path = 'E:\\BridgeChat\\BridgeChat.SharedLibraries\\Core.Contracts\\Responses\\ApiResponse.cs'
if os.path.exists(api_res_path):
    with open(api_res_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'public class ApiResponse<T>' in content:
        content = content.replace('public class ApiResponse<T>', 'public record ApiResponse<T>')
        with open(api_res_path, 'w', encoding='utf-8', newline='') as f:
            f.write(content)
        print("Fixed Rule 3 in ApiResponse.cs (changed to record)")

# 5. Sửa lỗi Rule 3 & Rule 4 tại 3 Validator của GroupService
group_val_dir = 'E:\\BridgeChat\\BridgeChat.GroupService\\BridgeChat.GroupService.Application\\Features\\Groups'
for root, dirs, files in os.walk(group_val_dir):
    for file in files:
        if file.endswith('Validator.cs'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            if 'SharedLibraries.Core.Localization.GlobalResource' in content:
                if 'using BridgeChat.SharedLibraries.Core.Localization;' not in content:
                    content = 'using BridgeChat.SharedLibraries.Core.Localization;\r\n' + content
                content = content.replace('SharedLibraries.Core.Localization.GlobalResource', 'GlobalResource')
                with open(filepath, 'w', encoding='utf-8', newline='') as f:
                    f.write(content)
                print(f"Fixed Rule 3/4 in {file}")

# 6. Sửa lỗi Rule 3 tại 10 Validator của UserService
user_vals = {
    'BlockUserCommandValidator.cs': [
        ('RuleFor(x => x.BlockerId)\n            .NotEmpty();', 'RuleFor(x => x.BlockerId)\n            .NotEmpty().WithMessage(localizer["VAL_BLOCKER_ID_REQUIRED"]);'),
        ('RuleFor(x => x.BlockedId)\n            .NotEmpty();', 'RuleFor(x => x.BlockedId)\n            .NotEmpty().WithMessage(localizer["VAL_BLOCKED_ID_REQUIRED"]);'),
        ('public BlockUserCommandValidator()', 'public BlockUserCommandValidator(IStringLocalizer<GlobalResource> localizer)')
    ],
    'UnblockUserCommandValidator.cs': [
        ('RuleFor(x => x.BlockerId)\n            .NotEmpty();', 'RuleFor(x => x.BlockerId)\n            .NotEmpty().WithMessage(localizer["VAL_BLOCKER_ID_REQUIRED"]);'),
        ('RuleFor(x => x.BlockedId)\n            .NotEmpty();', 'RuleFor(x => x.BlockedId)\n            .NotEmpty().WithMessage(localizer["VAL_BLOCKED_ID_REQUIRED"]);'),
        ('public UnblockUserCommandValidator()', 'public UnblockUserCommandValidator(IStringLocalizer<GlobalResource> localizer)')
    ],
    'GetBlockedUsersQueryValidator.cs': [
        ('RuleFor(x => x.BlockerId)\n            .NotEmpty();', 'RuleFor(x => x.BlockerId)\n            .NotEmpty().WithMessage(localizer["VAL_BLOCKER_ID_REQUIRED"]);'),
        ('public GetBlockedUsersQueryValidator()', 'public GetBlockedUsersQueryValidator(IStringLocalizer<GlobalResource> localizer)')
    ],
    'DeleteContactCommandValidator.cs': [
        ('RuleFor(x => x.ContactId)\n            .NotEmpty();', 'RuleFor(x => x.ContactId)\n            .NotEmpty().WithMessage(localizer["VAL_CONTACT_ID_REQUIRED"]);'),
        ('public DeleteContactCommandValidator()', 'public DeleteContactCommandValidator(IStringLocalizer<GlobalResource> localizer)')
    ],
    'GetContactsQueryValidator.cs': [
        ('RuleFor(x => x.UserId)\n            .NotEmpty();', 'RuleFor(x => x.UserId)\n            .NotEmpty().WithMessage(localizer["VAL_USER_ID_REQUIRED"]);'),
        ('public GetContactsQueryValidator()', 'public GetContactsQueryValidator(IStringLocalizer<GlobalResource> localizer)')
    ],
    'CheckUsernameAvailabilityQueryValidator.cs': [
        ('RuleFor(x => x.Username)\n            .NotEmpty();', 'RuleFor(x => x.Username)\n            .NotEmpty().WithMessage(localizer["VAL_USERNAME_REQUIRED"]);'),
        ('public CheckUsernameAvailabilityQueryValidator()', 'public CheckUsernameAvailabilityQueryValidator(IStringLocalizer<GlobalResource> localizer)')
    ],
    'GetMyProfileQueryValidator.cs': [
        ('RuleFor(x => x.UserId)\n            .NotEmpty();', 'RuleFor(x => x.UserId)\n            .NotEmpty().WithMessage(localizer["VAL_USER_ID_REQUIRED"]);'),
        ('public GetMyProfileQueryValidator()', 'public GetMyProfileQueryValidator(IStringLocalizer<GlobalResource> localizer)')
    ],
    'GetUserProfileQueryValidator.cs': [
        ('RuleFor(x => x.TargetUserId)\n            .NotEmpty();', 'RuleFor(x => x.TargetUserId)\n            .NotEmpty().WithMessage(localizer["VAL_USER_ID_REQUIRED"]);'),
        ('public GetUserProfileQueryValidator()', 'public GetUserProfileQueryValidator(IStringLocalizer<GlobalResource> localizer)')
    ],
    'GetMySettingQueryValidator.cs': [
        ('RuleFor(x => x.UserId)\n            .NotEmpty();', 'RuleFor(x => x.UserId)\n            .NotEmpty().WithMessage(localizer["VAL_USER_ID_REQUIRED"]);'),
        ('public GetMySettingQueryValidator()', 'public GetMySettingQueryValidator(IStringLocalizer<GlobalResource> localizer)')
    ]
}

user_val_dir = 'E:\\BridgeChat\\BridgeChat.UserService\\BridgeChat.UserService.Application\\Features'
for root, dirs, files in os.walk(user_val_dir):
    for file in files:
        if file in user_vals:
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'using Microsoft.Extensions.Localization;' not in content:
                content = 'using Microsoft.Extensions.Localization;\r\nusing BridgeChat.SharedLibraries.Core.Localization;\r\n' + content
            
            for old_str, new_str in user_vals[file]:
                # If exact replace fails due to whitespace/CRLF, use regex
                if old_str in content:
                    content = content.replace(old_str, new_str)
                else:
                    # Normalize CRLF for matching
                    old_regex = re.escape(old_str).replace(r'\r?\n', r'\s+')
                    content = re.sub(re.escape(old_str).replace(r'\n', r'\r?\n\s*'), new_str, content)
            
            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                f.write(content)
            print(f"Fixed Rule 3 in UserService {file}")

print("All minor errors fixed successfully!")
