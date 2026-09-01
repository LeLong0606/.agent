[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$SourceRoot,
    [string]$AgentRoot = (Split-Path $PSScriptRoot -Parent),
    [string]$OutputPath = (Join-Path (Split-Path $PSScriptRoot -Parent) 'sources/skill-survey.json')
)

$ErrorActionPreference = 'Stop'

function Read-FrontmatterValue {
    param([string[]]$Lines, [string]$Key)

    $start = -1
    for ($i = 0; $i -lt $Lines.Count; $i++) {
        if ($Lines[$i] -match "^$([regex]::Escape($Key)):\s*(.*)$") {
            $start = $i
            $value = $Matches[1].Trim()
            break
        }
    }
    if ($start -lt 0) { return '' }

    if ($value -in @('>', '>-', '|', '|-')) {
        $parts = [System.Collections.Generic.List[string]]::new()
        for ($i = $start + 1; $i -lt $Lines.Count; $i++) {
            if ($Lines[$i] -match '^\S[^:]*:\s*') { break }
            $part = $Lines[$i].Trim()
            if ($part) { $parts.Add($part) }
        }
        return ($parts -join ' ')
    }

    return $value.Trim('"', "'")
}

if (-not (Test-Path -LiteralPath $SourceRoot -PathType Container)) {
    throw "Missing source root: $SourceRoot"
}

$localNames = @{}
Get-ChildItem -LiteralPath (Join-Path $AgentRoot 'skills') -Directory | ForEach-Object {
    $localSkill = Join-Path $_.FullName 'SKILL.md'
    if (Test-Path -LiteralPath $localSkill -PathType Leaf) {
        $localNames[$_.Name] = $true
    }
}

$rawEntries = [System.Collections.Generic.List[object]]::new()
Get-ChildItem -LiteralPath $SourceRoot -Directory | ForEach-Object {
    $repo = $_
    Get-ChildItem -LiteralPath $repo.FullName -Recurse -Filter 'SKILL.md' -File -ErrorAction SilentlyContinue | ForEach-Object {
        $lines = Get-Content -LiteralPath $_.FullName -TotalCount 120
        $name = Read-FrontmatterValue $lines 'name'
        if (-not $name) { $name = Split-Path $_.DirectoryName -Leaf }
        $description = Read-FrontmatterValue $lines 'description'
        $relative = $_.FullName.Substring($repo.FullName.Length + 1).Replace('\', '/')
        $bodySample = ($lines -join "`n")
        $rawEntries.Add([pscustomobject]@{
            repo = $repo.Name
            name = $name
            description = $description
            path = $relative
            platformSpecific = [bool]($relative -match '^\.(claude|cursor|gemini|grok|openclaw)/' -or $bodySample -match 'CLAUDE_PLUGIN_ROOT|Claude session|AskUserQuestion')
        })
    }
}

$survey = $rawEntries | Group-Object repo, name | ForEach-Object {
    $preferred = $_.Group | Sort-Object @{
        Expression = {
            if ($_.path -match '^skills/[^/]+/SKILL\.md$') { 0 }
            elseif ($_.path -eq 'SKILL.md') { 1 }
            elseif ($_.path -match '^\.agents?/skills/') { 2 }
            else { 3 }
        }
    }, path | Select-Object -First 1

    $classification = if ($localNames.ContainsKey($preferred.name)) {
        'installed-or-overlap'
    }
    elseif ($preferred.repo -eq 'Front-End-Checklist') {
        'distilled-corpus'
    }
    elseif ($preferred.platformSpecific) {
        'runtime-specific-review'
    }
    else {
        'candidate-review'
    }

    [pscustomobject]@{
        repo = $preferred.repo
        name = $preferred.name
        description = $preferred.description
        canonicalPath = $preferred.path
        duplicateCopies = $_.Count
        classification = $classification
    }
} | Sort-Object repo, name

$payload = [pscustomobject]@{
    generatedAt = (Get-Date).ToString('o')
    sourceRootHint = 'Pass the current upstream clone root to regenerate; installed skills do not depend on it.'
    repositories = (Get-ChildItem -LiteralPath $SourceRoot -Directory).Count
    discoveredSkillFiles = $rawEntries.Count
    uniqueRepoSkills = $survey.Count
    classifications = @($survey | Group-Object classification | Sort-Object Name | ForEach-Object {
        [pscustomobject]@{ name = $_.Name; count = $_.Count }
    })
    skills = @($survey)
}

$payload | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $OutputPath -Encoding utf8NoBOM
$payload.classifications | Format-Table -AutoSize
Write-Output "Survey written: $OutputPath"
