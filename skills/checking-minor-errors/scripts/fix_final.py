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
        
    new_content = content.replace(
        'throw new InvalidOperationException($"Connection string \'DefaultConnection\' not found in configuration.");',
        'throw new InvalidOperationException(nameof(connectionString));'
    )
    
    with open(file, 'w', encoding='utf-8', newline='') as f:
        f.write(new_content)

otp_file = 'E:\\BridgeChat\\BridgeChat.NotificationService\\BridgeChat.NotificationService.Application\\IntegrationEvents\\Consumers\\OtpGeneratedEventConsumer.cs'
with open(otp_file, 'r', encoding='utf-8') as f:
    otp_content = f.read()
    
otp_content = otp_content.replace(
    '_logger.LogInformation("\\n{SimulatedSms}\\n", simulatedSms);',
    '_logger.LogInformation(System.Environment.NewLine + "{SimulatedSms}" + System.Environment.NewLine, simulatedSms);'
)

with open(otp_file, 'w', encoding='utf-8', newline='') as f:
    f.write(otp_content)
    
