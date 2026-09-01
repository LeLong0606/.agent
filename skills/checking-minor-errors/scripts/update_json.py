import json
import os
import re

keys = {
    'EXC_DB_CONNECTION_STRING_NOT_FOUND': {
        'en-US': 'Connection string \"DefaultConnection\" not found in configuration.',
        'vi-VN': 'Không tìm thấy chuỗi kết nối \"DefaultConnection\" trong cấu hình.',
        'zh-CN': '配置中未找到连接字符串 \"DefaultConnection\"。'
    },
    'EXC_ATTACHMENT_NOT_FOUND_OR_FORBIDDEN': {
        'en-US': 'One or more attachments do not exist or you do not have permission to access them.',
        'vi-VN': 'Một hoặc nhiều tệp đính kèm không tồn tại hoặc bạn không có quyền truy cập.',
        'zh-CN': '一个或多个附件不存在或您没有访问权限。'
    },
    'EXC_ATTACHMENT_NOT_READY': {
        'en-US': 'Attachment {0} has not finished uploading or encountered an error.',
        'vi-VN': 'Tệp đính kèm {0} chưa hoàn tất tải lên hoặc bị lỗi.',
        'zh-CN': '附件 {0} 尚未完成上传或遇到错误。'
    },
    'LOG_ELASTICSEARCH_SEARCH_ERROR': {
        'en-US': 'Error searching on Elasticsearch: {0}',
        'vi-VN': 'Lỗi khi tìm kiếm trên Elasticsearch: {0}',
        'zh-CN': '在 Elasticsearch 上搜索时出错: {0}'
    },
    'LOG_SEARCH_MSG_DEL_RECEIVED': {
        'en-US': 'Received MessageDeletedEvent for MessageId: {0}',
        'vi-VN': 'Nhận được sự kiện MessageDeletedEvent cho MessageId: {0}',
        'zh-CN': '收到 MessageId: {0} 的 MessageDeletedEvent 事件'
    },
    'LOG_SEARCH_MSG_DEL_SUCCESS': {
        'en-US': 'Successfully deleted message {0} from Elasticsearch.',
        'vi-VN': 'Đã xóa thành công tin nhắn {0} khỏi Elasticsearch.',
        'zh-CN': '已成功从 Elasticsearch 中删除消息 {0}。'
    },
    'LOG_SEARCH_MSG_DEL_NOT_FOUND': {
        'en-US': 'Message {0} not found on Elasticsearch to delete.',
        'vi-VN': 'Không tìm thấy tin nhắn {0} trên Elasticsearch để xóa.',
        'zh-CN': '在 Elasticsearch 上未找到要删除的消息 {0}。'
    },
    'LOG_SEARCH_MSG_DEL_ERROR': {
        'en-US': 'Error deleting message {0} on Elasticsearch: {1}',
        'vi-VN': 'Lỗi khi xóa tin nhắn {0} trên Elasticsearch: {1}',
        'zh-CN': '在 Elasticsearch 上删除消息 {0} 时出错: {1}'
    },
    'LOG_SEARCH_MSG_DEL_EXCEPTION': {
        'en-US': 'Exception occurred while processing MessageDeletedEvent for MessageId: {0}',
        'vi-VN': 'Ngoại lệ xảy ra khi xử lý sự kiện MessageDeletedEvent cho MessageId: {0}',
        'zh-CN': '处理 MessageId: {0} 的 MessageDeletedEvent 事件时发生异常'
    },
    'LOG_SEARCH_MSG_EDIT_RECEIVED': {
        'en-US': 'Received MessageEditedEvent for MessageId: {0}',
        'vi-VN': 'Nhận được sự kiện MessageEditedEvent cho MessageId: {0}',
        'zh-CN': '收到 MessageId: {0} 的 MessageEditedEvent 事件'
    },
    'LOG_SEARCH_MSG_EDIT_SUCCESS': {
        'en-US': 'Successfully updated message {0} on Elasticsearch.',
        'vi-VN': 'Đã cập nhật thành công tin nhắn {0} trên Elasticsearch.',
        'zh-CN': '已成功在 Elasticsearch 上更新消息 {0}。'
    },
    'LOG_SEARCH_MSG_EDIT_ERROR': {
        'en-US': 'Error updating message {0} on Elasticsearch: {1}',
        'vi-VN': 'Lỗi khi cập nhật tin nhắn {0} trên Elasticsearch: {1}',
        'zh-CN': '在 Elasticsearch 上更新消息 {0} 时出错: {1}'
    },
    'LOG_SEARCH_MSG_EDIT_EXCEPTION': {
        'en-US': 'Exception occurred while processing MessageEditedEvent for MessageId: {0}',
        'vi-VN': 'Ngoại lệ xảy ra khi xử lý sự kiện MessageEditedEvent cho MessageId: {0}',
        'zh-CN': '处理 MessageId: {0} 的 MessageEditedEvent 事件时发生异常'
    },
    'LOG_LMSTUDIO_RESPONSE_EMPTY_VECTOR': {
        'en-US': 'LM Studio returned a valid response but it does not contain an embedding vector.',
        'vi-VN': 'LM Studio trả về response hợp lệ nhưng không chứa vector embedding.',
        'zh-CN': 'LM Studio 返回了有效的响应，但不包含嵌入向量。'
    },
    'LOG_LMSTUDIO_API_ERROR': {
        'en-US': 'Error calling LM Studio API to generate embedding vector.',
        'vi-VN': 'Lỗi khi gọi LM Studio API để sinh vector embedding.',
        'zh-CN': '调用 LM Studio API 生成嵌入向量时出错。'
    },
    'LOG_AVATAR_ATTACHMENT_INVALID': {
        'en-US': 'AttachmentId {0} does not exist or is inaccessible.',
        'vi-VN': 'AttachmentId {0} không tồn tại hoặc không thể truy cập.',
        'zh-CN': 'AttachmentId {0} 不存在或无法访问。'
    },
    'EXC_AVATAR_MUST_BE_IMAGE': {
        'en-US': 'Avatar must be a valid image file (jpg, png, webp, ...).',
        'vi-VN': 'Ảnh đại diện phải là một tệp hình ảnh hợp lệ (jpg, png, webp, ...).',
        'zh-CN': '头像必须是有效的图像文件 (jpg, png, webp, ...)。'
    },
    'LOG_USER_AVATAR_CHANGED': {
        'en-US': 'User {0} successfully changed their avatar. New URL: {1}',
        'vi-VN': 'Người dùng {0} vừa thay đổi ảnh đại diện thành công. URL mới: {1}',
        'zh-CN': '用户 {0} 成功更改了头像。新 URL: {1}'
    }
}

for lang in ['en-US', 'vi-VN', 'zh-CN']:
    filepath = f'E:\\BridgeChat\\BridgeChat.SharedLibraries\\Core.Localization\\Resources\\{lang}.json'
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for k, v in keys.items():
        data[k] = v[lang]
        
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    json_str = json_str.replace('\r\n', '\n').replace('\n', '\r\n')
    
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        f.write(json_str + '\r\n')
    print(f'Updated {lang}.json')
