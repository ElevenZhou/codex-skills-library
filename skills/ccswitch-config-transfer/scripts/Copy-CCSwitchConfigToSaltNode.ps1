param(
    [Parameter(Mandatory = $true)]
    [string]$TargetNodeId,

    [string]$TargetUser = "april",

    [string]$SourceConfigDir = (Join-Path $HOME ".cc-switch"),

    [string]$BackupRoot = (Join-Path (Get-Location) "backups"),

    [Parameter(Mandatory = $true)]
    [string]$MasterHost,

    [string]$MasterUser = "ubuntu",

    [Parameter(Mandatory = $true)]
    [string]$MasterKey,

    [Parameter(Mandatory = $true)]
    [string]$BindAddress,

    [string]$RemoteTransferDir = "/srv/salt/_transfer"
)

$ErrorActionPreference = "Stop"

function Invoke-Native {
    param(
        [Parameter(Mandatory = $true)]
        [string]$FilePath,

        [Parameter(Mandatory = $true)]
        [string[]]$Arguments
    )

    & $FilePath @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "$FilePath failed with exit code $LASTEXITCODE"
    }
}

function Require-File {
    param([string]$Path)
    if (!(Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "Required file not found: $Path"
    }
}

function Require-Directory {
    param([string]$Path)
    if (!(Test-Path -LiteralPath $Path -PathType Container)) {
        throw "Required directory not found: $Path"
    }
}

$TargetNodeId = $TargetNodeId.Trim().ToUpperInvariant()
if ($TargetNodeId -notmatch "^[A-Z]{1,4}[0-9]{2,3}$") {
    throw "Bad TargetNodeId: $TargetNodeId"
}

Require-Directory $SourceConfigDir
Require-File (Join-Path $SourceConfigDir "cc-switch.db")
Require-File (Join-Path $SourceConfigDir "settings.json")
Require-File $MasterKey

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backupRootFull = [System.IO.Path]::GetFullPath($BackupRoot)
$runRoot = Join-Path $backupRootFull ("ccswitch-" + $timestamp)
$stageRoot = Join-Path $runRoot "payload"
$stageConfig = Join-Path $stageRoot ".cc-switch"

New-Item -ItemType Directory -Force -Path $stageConfig | Out-Null

Copy-Item -LiteralPath (Join-Path $SourceConfigDir "cc-switch.db") -Destination (Join-Path $stageConfig "cc-switch.db") -Force
Copy-Item -LiteralPath (Join-Path $SourceConfigDir "settings.json") -Destination (Join-Path $stageConfig "settings.json") -Force

$copilot = Join-Path $SourceConfigDir "copilot_auth.json"
if (Test-Path -LiteralPath $copilot -PathType Leaf) {
    Copy-Item -LiteralPath $copilot -Destination (Join-Path $stageConfig "copilot_auth.json") -Force
}

$skills = Join-Path $SourceConfigDir "skills"
if (Test-Path -LiteralPath $skills -PathType Container) {
    Copy-Item -LiteralPath $skills -Destination (Join-Path $stageConfig "skills") -Recurse -Force
}

$manifest = [ordered]@{
    created_at = (Get-Date).ToString("s")
    source = $SourceConfigDir
    target_node = $TargetNodeId
    target_user = $TargetUser
    contents = @("cc-switch.db", "settings.json", "copilot_auth.json", "skills")
}
$manifest | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $stageRoot "manifest.json") -Encoding UTF8

$zipPath = Join-Path $backupRootFull ("ccswitch-" + $timestamp + ".zip")
Compress-Archive -LiteralPath (Join-Path $stageRoot ".cc-switch"), (Join-Path $stageRoot "manifest.json") -DestinationPath $zipPath -Force

$localHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $zipPath).Hash.ToLowerInvariant()
$masterTarget = "/tmp/ccswitch-$TargetNodeId.zip"
$saltUrl = "salt://_transfer/ccswitch-$TargetNodeId.zip"
$nodeTarget = "/tmp/ccswitch-$TargetNodeId.zip"

$sshBaseArgs = @()
if ($BindAddress) {
    $sshBaseArgs += @("-b", $BindAddress)
}
$sshBaseArgs += @("-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes", "-i", $MasterKey)

$scpArgs = @()
if ($BindAddress) {
    $scpArgs += @("-o", "BindAddress=$BindAddress")
}
$scpArgs += @("-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes", "-i", $MasterKey, $zipPath, "$MasterUser@$MasterHost`:$masterTarget")

Write-Host "Uploading local archive to Salt master: $zipPath"
Invoke-Native -FilePath "scp" -Arguments $scpArgs

$publishCommand = "sudo mkdir -p '$RemoteTransferDir' && sudo cp '$masterTarget' '$RemoteTransferDir/ccswitch-$TargetNodeId.zip' && sudo salt -t 120 $TargetNodeId cp.get_file '$saltUrl' '$nodeTarget' makedirs=True"
Invoke-Native -FilePath "ssh" -Arguments ($sshBaseArgs + @("$MasterUser@$MasterHost", $publishCommand))

$checkCommand = "sudo salt -t 60 $TargetNodeId cmd.run 'shasum -a 256 $nodeTarget' runas=$TargetUser"
$checkOutput = & ssh @sshBaseArgs "$MasterUser@$MasterHost" $checkCommand
if ($LASTEXITCODE -ne 0) {
    throw "Remote checksum command failed"
}
$checkOutput | Write-Host
if (($checkOutput -join "`n").ToLowerInvariant() -notmatch [regex]::Escape($localHash)) {
    throw "Remote checksum did not match local hash $localHash"
}

$restoreScript = @"
set -e
TS=`$(date +%Y%m%d-%H%M%S)
HOME_DIR=`$(dscl . -read /Users/$TargetUser NFSHomeDirectory 2>/dev/null | awk '{print `$2}')
if [ -z "`$HOME_DIR" ]; then HOME_DIR="/Users/$TargetUser"; fi
TARGET_DIR="`$HOME_DIR/.cc-switch"
BACKUP_DIR="`$HOME_DIR/.cc-switch.restore-backups/`$TS"
if [ "`$TARGET_DIR" != "`$HOME_DIR/.cc-switch" ]; then
  echo "refusing unsafe target: `$TARGET_DIR" >&2
  exit 2
fi
mkdir -p "`$BACKUP_DIR"
if [ -d "`$TARGET_DIR" ]; then
  ditto -c -k --sequesterRsrc --keepParent "`$TARGET_DIR" "`$BACKUP_DIR/cc-switch-before-restore.zip"
fi
pkill -f 'com.ccswitch.desktop|ccswitch|cc-switch' 2>/dev/null || true
rm -rf /tmp/ccswitch-restore
mkdir -p /tmp/ccswitch-restore
unzip -oq "$nodeTarget" -d /tmp/ccswitch-restore
if [ ! -f /tmp/ccswitch-restore/.cc-switch/cc-switch.db ]; then
  echo "restore payload missing cc-switch.db" >&2
  exit 3
fi
rm -rf "`$TARGET_DIR"
ditto /tmp/ccswitch-restore/.cc-switch "`$TARGET_DIR"
chmod -R u+rwX "`$TARGET_DIR"
echo "backup=`$BACKUP_DIR/cc-switch-before-restore.zip"
find "`$TARGET_DIR" -maxdepth 2 -type f | sed "s#^`$HOME_DIR/##" | sort
if command -v sqlite3 >/dev/null 2>&1; then
  sqlite3 "`$TARGET_DIR/cc-switch.db" "PRAGMA integrity_check;"
else
  echo "sqlite3-unavailable"
fi
"@

$encodedRestore = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($restoreScript))
$restoreCommand = "sudo salt -t 120 $TargetNodeId cmd.run 'printf %s $encodedRestore | base64 -d | bash' runas=$TargetUser"
Invoke-Native -FilePath "ssh" -Arguments ($sshBaseArgs + @("$MasterUser@$MasterHost", $restoreCommand))

Write-Host ""
Write-Host "Done."
Write-Host "Local archive: $zipPath"
Write-Host "SHA256: $localHash"
