# PDF to Excel Converter - Windows PowerShell Deployment Script (SCP + Minimal SSH)
# Usage: .\deploy.ps1 [server_ip] [ssh_user]
# Note: This script minimizes password prompts by using SCP for file transfer and single SSH for permissions

param(
    [string]$ServerIP = "45.32.105.73",
    [string]$SSHUser = "aan"
)

# Configuration
$LocalFile = "dist\index-oneliner.html"
$RemotePath = "/var/www/html/pdf-to-excel"

# Functions
function Write-Info($message) { Write-Host "[INFO] $message" -ForegroundColor Blue }
function Write-Success($message) { Write-Host "[SUCCESS] $message" -ForegroundColor Green }
function Write-Error($message) { Write-Host "[ERROR] $message" -ForegroundColor Red }

Write-Info "Starting deployment to $SSHUser@$ServerIP"

# Check if local file exists
if (-not (Test-Path $LocalFile)) {
    Write-Error "Local file $LocalFile not found!"
    Write-Info "Run 'npm run build' first to create the production file"
    exit 1
}

Write-Success "Found local file: $LocalFile"

# Show file info
$FileSize = (Get-Item $LocalFile).Length
$FileSizeMB = [math]::Round($FileSize / 1KB, 2)
Write-Info "File size: $FileSizeMB KB"

# Upload file to temporary location via SCP (first password prompt)
Write-Info "Uploading file to temporary location (you will be prompted for password)..."
scp $LocalFile "${SSHUser}@${ServerIP}:/tmp/index.html"

if ($LASTEXITCODE -ne 0) {
    Write-Error "File upload failed"
    exit 1
}

Write-Success "File uploaded to temporary location"

# Prompt for sudo password
Write-Info "Please enter sudo password for user $SSHUser on server $ServerIP"
$SudoPass = Read-Host "Sudo password" -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($SudoPass)
$PlainSudoPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
[System.Runtime.InteropServices.Marshal]::FreeBSTR($BSTR)

# Move file to final location and set permissions via SSH (second password prompt)
Write-Info "Moving file to final location and setting permissions (you will be prompted for password)..."
$MoveCommands = @"
echo "=== Starting file deployment ==="
echo "Creating directory if needed..."
if echo '$PlainSudoPassword' | sudo -S mkdir -p $RemotePath; then
    echo "SUCCESS: Directory created or already exists"
else
    echo "ERROR: Failed to create directory"
    exit 1
fi

echo "Moving file to final location..."
if echo '$PlainSudoPassword' | sudo -S mv /tmp/index.html $RemotePath/index.html; then
    echo "SUCCESS: File moved to final location"
else
    echo "ERROR: Failed to move file"
    exit 1
fi

echo "Setting file ownership..."
if echo '$PlainSudoPassword' | sudo -S chown www-data:www-data $RemotePath/index.html; then
    echo "SUCCESS: File ownership set"
else
    echo "ERROR: Failed to set file ownership"
    exit 1
fi

echo "Setting file permissions..."
if echo '$PlainSudoPassword' | sudo -S chmod 644 $RemotePath/index.html; then
    echo "SUCCESS: File permissions set"
else
    echo "ERROR: Failed to set file permissions"
    exit 1
fi

echo "Verifying file exists..."
if [ -f "$RemotePath/index.html" ]; then
    echo "SUCCESS: File successfully deployed to $RemotePath/index.html"
    ls -l $RemotePath/index.html
else
    echo "ERROR: File not found at $RemotePath/index.html"
    exit 1
fi
echo "=== File deployment completed ==="
"@

Write-Info "Executing remote commands..."
$Result = ssh "${SSHUser}@${ServerIP}" $MoveCommands
$ExitCode = $LASTEXITCODE

Write-Info "SSH command output:"
Write-Host $Result

if ($ExitCode -eq 0) {
    # Check if the result contains the success message
    if ($Result -like "*SUCCESS: File successfully deployed*") {
        Write-Success "File successfully deployed to $RemotePath/index.html"
        Write-Info "Access via: http://$ServerIP/pdf-to-excel/index.html"
        Write-Info "Local file size: $FileSizeMB KB"
        Write-Success "Deployment completed successfully with only two password entries!"
    } else {
        Write-Error "Failed to move file to final location"
        Write-Error "Command output: $Result"
        exit 1
    }
} else {
    Write-Error "SSH command failed with exit code: $ExitCode"
    Write-Error "Command output: $Result"
    exit 1
}