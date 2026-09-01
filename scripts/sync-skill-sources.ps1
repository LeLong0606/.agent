[CmdletBinding()]
param(
    [ValidateSet('Audit', 'Sync')]
    [string]$Mode = 'Audit',
    [string]$SourceRoot = $env:AGENT_SKILL_SOURCE_ROOT,
    [string]$AgentRoot = (Split-Path $PSScriptRoot -Parent)
)

$ErrorActionPreference = 'Stop'

$manifestPath = Join-Path $AgentRoot 'sources/skill-sources.json'
$targetRoot = Join-Path $AgentRoot 'skills'

if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) {
    throw "Missing source manifest: $manifestPath"
}
if ([string]::IsNullOrWhiteSpace($SourceRoot)) {
    throw 'SourceRoot is required only for upstream audit/sync. Pass -SourceRoot or set AGENT_SKILL_SOURCE_ROOT. Installed skills under AgentRoot/skills remain standalone.'
}
if (-not (Test-Path -LiteralPath $SourceRoot -PathType Container)) {
    throw "Missing optional upstream skill source root: $SourceRoot"
}
if (-not (Test-Path -LiteralPath $targetRoot -PathType Container)) {
    throw "Missing agent skills directory: $targetRoot"
}

$manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
$plan = [System.Collections.Generic.List[object]]::new()

function Get-PayloadFingerprint {
    param([string]$Path)

    $excludedNames = @(
        '.git', '.github', '.gitea', '.vscode', '.idea',
        '.claude', '.cursor', '.agents', '.agent', '.gemini', '.grok', '.openclaw',
        'node_modules', '__pycache__'
    )
    $root = (Resolve-Path -LiteralPath $Path).Path
    $records = Get-ChildItem -LiteralPath $root -Recurse -Force -File | Where-Object {
        $relative = $_.FullName.Substring($root.Length).TrimStart('\', '/')
        -not (($relative -split '[\\/]') | Where-Object { $_ -in $excludedNames })
    } | ForEach-Object {
        $relative = $_.FullName.Substring($root.Length).TrimStart('\', '/').Replace('\', '/')
        "$relative|$((Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash)"
    } | Sort-Object

    $joined = $records -join "`n"
    $bytes = [Text.Encoding]::UTF8.GetBytes($joined)
    $hash = [Security.Cryptography.SHA256]::HashData($bytes)
    return [Convert]::ToHexString($hash)
}

function Add-PlanItem {
    param(
        [string]$Repo,
        [string]$Source,
        [string]$Target,
        [string]$Policy
    )

    $skillFile = Join-Path $Source 'SKILL.md'
    $status = if (-not (Test-Path -LiteralPath $skillFile -PathType Leaf)) {
        'INVALID_SOURCE'
    }
    elseif (Test-Path -LiteralPath $Target -PathType Container) {
        if ((Get-PayloadFingerprint $Source) -eq (Get-PayloadFingerprint $Target)) {
            'SYNCED'
        }
        else {
            'EXISTS_REVIEW'
        }
    }
    else {
        'NEW'
    }

    $plan.Add([pscustomobject]@{
        Repo = $Repo
        Status = $status
        Policy = $Policy
        Name = Split-Path $Target -Leaf
        Source = $Source
        Target = $Target
    })
}

function Copy-SkillPayload {
    param(
        [string]$Source,
        [string]$Target
    )

    $excludedNames = @(
        '.git', '.github', '.gitea', '.vscode', '.idea',
        '.claude', '.cursor', '.agents', '.agent', '.gemini', '.grok', '.openclaw',
        'node_modules', '__pycache__'
    )

    New-Item -ItemType Directory -Path $Target | Out-Null
    Get-ChildItem -LiteralPath $Source -Force | Where-Object {
        $_.Name -notin $excludedNames
    } | ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination $Target -Recurse
    }
}

foreach ($collection in $manifest.collections) {
    $repoRoot = Join-Path $SourceRoot $collection.repo
    $collectionRoot = Join-Path $repoRoot $collection.root
    if (-not (Test-Path -LiteralPath $collectionRoot -PathType Container)) {
        $plan.Add([pscustomobject]@{
            Repo = $collection.repo
            Status = 'MISSING_REPO'
            Policy = $collection.mode
            Name = '*'
            Source = $collectionRoot
            Target = $targetRoot
        })
        continue
    }

    Get-ChildItem -LiteralPath $collectionRoot -Directory | ForEach-Object {
        if (Test-Path -LiteralPath (Join-Path $_.FullName 'SKILL.md') -PathType Leaf) {
            Add-PlanItem -Repo $collection.repo -Source $_.FullName -Target (Join-Path $targetRoot $_.Name) -Policy $collection.mode
        }
    }
}

foreach ($single in $manifest.singles) {
    $repoRoot = Join-Path $SourceRoot $single.repo
    $source = if ($single.path -eq '.') { $repoRoot } else { Join-Path $repoRoot $single.path }
    Add-PlanItem -Repo $single.repo -Source $source -Target (Join-Path $targetRoot $single.target) -Policy $single.mode
}

if ($Mode -eq 'Sync') {
    foreach ($item in $plan | Where-Object Status -eq 'NEW') {
        Copy-SkillPayload -Source $item.Source -Target $item.Target
    }
}

$plan | Sort-Object Status, Repo, Name | Format-Table Status, Repo, Name, Policy -AutoSize

$summary = $plan | Group-Object Status | Sort-Object Name | ForEach-Object {
    "{0}={1}" -f $_.Name, $_.Count
}
Write-Output ("Summary: " + ($summary -join ', '))

if ($plan.Status -contains 'INVALID_SOURCE' -or $plan.Status -contains 'MISSING_REPO') {
    exit 2
}
