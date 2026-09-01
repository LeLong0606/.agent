$services = @(
    "BridgeChat.APIGateway",
    "BridgeChat.AttachmentService",
    "BridgeChat.ConnectionService",
    "BridgeChat.GroupService",
    "BridgeChat.IdentityService",
    "BridgeChat.MessageService",
    "BridgeChat.NotificationService",
    "BridgeChat.PresenceService",
    "BridgeChat.SearchService",
    "BridgeChat.SharedLibraries",
    "BridgeChat.UserService",
    "bridgechatwebreact"
)

foreach ($service in $services) {
    $path = Join-Path -Path "E:\BridgeChat" -ChildPath $service
    if (Test-Path $path) {
        Set-Location $path
        Write-Host "Processing $service..." -ForegroundColor Cyan
        
        if (Test-Path (Join-Path $path ".git")) {
            $status = git status --porcelain
            if (![string]::IsNullOrWhiteSpace($status)) {
                Write-Host "Changes found in $service, committing and pushing..." -ForegroundColor Yellow
                git add .
                git commit -m "feat: upgrade conversation vault in-flow sidebar, telegram media album, and e2ee animations"
                git push origin master
                Write-Host "Pushed $service" -ForegroundColor Green
            } else {
                Write-Host "No changes in $service" -ForegroundColor DarkGray
            }
        } else {
            Write-Host "$service is not a git repository!" -ForegroundColor Red
        }
    }
}
Set-Location "E:\BridgeChat"
