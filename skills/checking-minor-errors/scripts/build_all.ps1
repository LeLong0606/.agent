$services = @(
    "BridgeChat.APIGateway\BridgeChat.APIGateway.slnx",
    "BridgeChat.AttachmentService\BridgeChat.AttachmentService.slnx",
    "BridgeChat.ConnectionService\BridgeChat.ConnectionService.slnx",
    "BridgeChat.GroupService\BridgeChat.GroupService.slnx",
    "BridgeChat.IdentityService\BridgeChat.IdentityService.slnx",
    "BridgeChat.MessageService\BridgeChat.MessageService.slnx",
    "BridgeChat.NotificationService\BridgeChat.NotificationService.slnx",
    "BridgeChat.PresenceService\BridgeChat.PresenceService.slnx",
    "BridgeChat.SearchService\BridgeChat.SearchService.slnx",
    "BridgeChat.SharedLibraries\BridgeChat.SharedLibraries.slnx",
    "BridgeChat.UserService\BridgeChat.UserService.slnx"
)

$hasError = $false

foreach ($service in $services) {
    $path = Join-Path -Path $PWD -ChildPath $service
    if (Test-Path $path) {
        Write-Host "Building $service..." -ForegroundColor Cyan
        dotnet build $path
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Build failed for $service" -ForegroundColor Red
            $hasError = $true
            break
        }
    } else {
        Write-Host "Could not find $service" -ForegroundColor Yellow
    }
}

if (-not $hasError) {
    Write-Host "All services built successfully!" -ForegroundColor Green
}
