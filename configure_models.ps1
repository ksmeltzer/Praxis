param (
    [string]$Provider = "github_copilot",
    [string]$ConfigFile = "$env:USERPROFILE\.config\opencode\opencode.json"
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$MappingsFile = Join-Path $RepoRoot "model-mappings.json"

if (-not (Test-Path $MappingsFile)) {
    Write-Error "Error: model-mappings.json not found in the current directory."
    exit 1
}

if (-not (Test-Path $ConfigFile)) {
    Write-Error "Error: Config file $ConfigFile not found. Please run this tool after initializing your agent framework, or specify the path with -ConfigFile"
    exit 1
}

Write-Host "Configuring models for provider '$Provider' in $ConfigFile..." -ForegroundColor Cyan

try {
    $Mappings = Get-Content $MappingsFile -Raw | ConvertFrom-Json
    
    if ($null -eq $Mappings.providers.$Provider) {
        $Available = $Mappings.providers.psobject.properties.Name -join ', '
        Write-Error "Error: Provider '$Provider' not found in model-mappings.json. Available providers: $Available"
        exit 1
    }

    $ProviderAgents = $Mappings.providers.$Provider.agent
    $TargetConfig = Get-Content $ConfigFile -Raw | ConvertFrom-Json

    if ($null -eq $TargetConfig.agent) {
        $TargetConfig | Add-Member -MemberType NoteProperty -Name "agent" -Value @{}
    }

    $Updated = $false
    foreach ($Agent in $ProviderAgents.psobject.properties) {
        $AgentName = $Agent.Name
        $AgentConfig = $Agent.Value

        if ($null -eq $TargetConfig.agent.$AgentName) {
            $TargetConfig.agent | Add-Member -MemberType NoteProperty -Name $AgentName -Value $AgentConfig
            $Updated = $true
        }
    }

    if ($Updated) {
        $TargetConfig | ConvertTo-Json -Depth 10 | Set-Content $ConfigFile
        Write-Host "Successfully updated agent mappings in $ConfigFile" -ForegroundColor Green
    } else {
        Write-Host "Agent mappings already exist in $ConfigFile. No changes made." -ForegroundColor Yellow
    }
} catch {
    Write-Error "Failed to process configuration: $_"
    exit 1
}
