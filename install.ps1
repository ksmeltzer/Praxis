param (
    [Parameter(Mandatory=$true)]
    [string]$Target,
    
    [ValidateSet("copy", "symlink")]
    [string]$Mode = "copy"
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$TargetDir = Resolve-Path -Path $Target -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Path
if (-not $TargetDir) {
    $TargetDir = Join-Path -Path (Get-Location) -ChildPath $Target
}

Write-Host "Installing Praxis to $TargetDir (Mode: $Mode)..." -ForegroundColor Cyan

$null = New-Item -ItemType Directory -Force -Path "$TargetDir\skills", "$TargetDir\commands", "$TargetDir\agent"

if ($Mode -eq "symlink") {
    try {
        $null = New-Item -ItemType Junction -Force -Path "$TargetDir\skills\praxis" -Target "$RepoRoot\skills\praxis"
        $null = New-Item -ItemType SymbolicLink -Force -Path "$TargetDir\commands\praxis.md" -Target "$RepoRoot\commands\praxis.md"
        $null = New-Item -ItemType Junction -Force -Path "$TargetDir\agent\praxis" -Target "$RepoRoot\agents\praxis"
        Write-Host "Symlinked Praxis to $TargetDir" -ForegroundColor Green
    } catch {
        Write-Warning "Symlinks require Administrator privileges on Windows."
        Write-Warning "Please run as Administrator, or run without --Mode symlink to use 'copy'."
        exit 1
    }
} else {
    Copy-Item -Recurse -Force "$RepoRoot\skills\praxis" "$TargetDir\skills\"
    Copy-Item -Force "$RepoRoot\commands\praxis.md" "$TargetDir\commands\"
    Copy-Item -Recurse -Force "$RepoRoot\agents\praxis" "$TargetDir\agent\"
    Write-Host "Copied Praxis to $TargetDir" -ForegroundColor Green
}

Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "  1. Run .\configure_models.ps1 -Provider <your_provider> to insert agent model mappings into your opencode.json."
Write-Host "  2. Restart your agent tool to load the /praxis command."
