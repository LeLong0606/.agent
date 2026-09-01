[CmdletBinding()]
param(
    [string]$CatalogPath,
    [string]$WindowTitlePattern = 'Antigravity',
    [int]$MinimumCharacters = 2,
    [switch]$ValidateOnly
)

$ErrorActionPreference = 'Stop'

if ($PSVersionTable.PSEdition -eq 'Core') {
    $windowsPowerShell = Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'
    $launchArguments = @(
        '-NoProfile',
        '-ExecutionPolicy', 'Bypass',
        '-File', $MyInvocation.MyCommand.Path,
        '-WindowTitlePattern', $WindowTitlePattern,
        '-MinimumCharacters', [string]$MinimumCharacters
    )
    if (-not [string]::IsNullOrWhiteSpace($CatalogPath)) {
        $launchArguments += @('-CatalogPath', $CatalogPath)
    }
    if ($ValidateOnly) { $launchArguments += '-ValidateOnly' }
    & $windowsPowerShell @launchArguments
    exit $LASTEXITCODE
}

$toolRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$agentRoot = Split-Path -Parent (Split-Path -Parent $toolRoot)

if ([string]::IsNullOrWhiteSpace($CatalogPath)) {
    $CatalogPath = Join-Path $agentRoot 'workflows/natural-language-triggers.md'
}

$CatalogPath = [System.IO.Path]::GetFullPath($CatalogPath)
if (-not (Test-Path -LiteralPath $CatalogPath -PathType Leaf)) {
    throw "Prompt catalog not found: $CatalogPath"
}

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
Add-Type -AssemblyName WindowsBase

$sourcePath = Join-Path $toolRoot 'PromptAutocomplete.cs'
$source = Get-Content -LiteralPath $sourcePath -Raw -Encoding UTF8
$runtimeReferences = [AppDomain]::CurrentDomain.GetAssemblies() |
    Where-Object { -not $_.IsDynamic -and $_.Location } |
    ForEach-Object Location |
    Sort-Object -Unique

Add-Type -TypeDefinition $source -Language CSharp -ReferencedAssemblies $runtimeReferences

if ($ValidateOnly) {
    Write-Output 'Prompt autocomplete compile: PASS'
    Write-Output "Catalog: $CatalogPath"
    Write-Output ([AgentPromptAutocomplete.Program]::ValidateLayoutMatrix())
    exit 0
}

[AgentPromptAutocomplete.Program]::Run(
    $CatalogPath,
    $WindowTitlePattern,
    [Math]::Max(2, $MinimumCharacters)
)
