# PDF to Excel Converter - Windows PowerShell Deployment Script
# Usage: .\deploy.ps1 [server_ip] [ssh_user]
# Note: This script uses password authentication for SSH/SCP

param(
    [string]$ServerIP = "45.32.105.73",
    [string]$SSHUser = "aan"
)

# Configuration
$LocalFile = "dist\index-oneliner.html"
$RemotePath = "/var/www/html/pdf-to-excel"
$ApacheSite = "pdf-to-excel.basangdata.com"

# Functions
function Write-Info($message) { Write-Host "[INFO] $message" -ForegroundColor Blue }
function Write-Success($message) { Write-Host "[SUCCESS] $message" -ForegroundColor Green }
function Write-Warning($message) { Write-Host "[WARNING] $message" -ForegroundColor Yellow }
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

# Prompt for SSH password
Write-Info "Please enter SSH password when prompted"

# Deploy the file
Write-Info "Deploying $LocalFile to production server..."

# Server preparation commands
$DeployCommands = @"
set -e

# Create directory if it doesn't exist
sudo mkdir -p $RemotePath
echo 'Created directory: $RemotePath'

# Set proper ownership
sudo chown www-data:www-data $RemotePath
echo 'Set ownership to www-data:www-data'

# Set proper permissions
sudo chmod 755 $RemotePath
echo 'Set directory permissions to 755'

# Enable Apache site if not already enabled
if ! sudo a2ensite $ApacheSite 2>/dev/null; then
    echo 'Site already enabled or configuration not found'
else
    echo 'Enabled Apache site: $ApacheSite'
fi

# Enable required Apache modules
sudo a2enmod headers rewrite
echo 'Enabled Apache modules: headers, rewrite'

# Reload Apache configuration
sudo systemctl reload apache2
echo 'Reloaded Apache configuration'

echo 'Server preparation complete'
"@

# Execute server preparation
Write-Info "Preparing server..."
Write-Info "Please enter password when prompted by SSH"
ssh "${SSHUser}@${ServerIP}" $DeployCommands

# Copy the file
Write-Info "Uploading file..."
Write-Info "Please enter password when prompted by SCP"
scp $LocalFile "${SSHUser}@${ServerIP}:/tmp/index.html"

# Move file to final location and set permissions
$FinalSetup = @"
set -e

# Move file to web directory
sudo mv /tmp/index.html $RemotePath/index.html
echo 'Moved file to $RemotePath/index.html'

# Set proper file ownership and permissions
sudo chown www-data:www-data $RemotePath/index.html
sudo chmod 644 $RemotePath/index.html
echo 'Set file permissions'

# Test Apache configuration
if sudo apache2ctl configtest; then
    echo 'Apache configuration is valid'
else
    echo 'Apache configuration has errors'
    exit 1
fi

# Final reload
sudo systemctl reload apache2
echo 'Final Apache reload complete'

echo 'Deployment successful!'
"@

ssh "${SSHUser}@${ServerIP}" $FinalSetup

# Verify deployment
Write-Info "Verifying deployment..."

$VerifyCommands = @"
# Check if file exists and get info
if [ -f '$RemotePath/index.html' ]; then
    FILE_SIZE=`$(ls -lh '$RemotePath/index.html' | awk '{print `$5}')
    FILE_OWNER=`$(ls -l '$RemotePath/index.html' | awk '{print `$3":"$4}')`
    echo "File deployed: `$FILE_SIZE, Owner: `$FILE_OWNER"
else
    echo 'ERROR: File not found at $RemotePath/index.html'
    exit 1
fi

# Test local HTTP response
HTTP_STATUS=`$(curl -s -o /dev/null -w '%{http_code}' -H 'Host: $ApacheSite' http://localhost/ || echo 'FAILED')
echo "Local HTTP test: `$HTTP_STATUS"

# Check Apache status
if systemctl is-active --quiet apache2; then
    echo 'Apache2 service: RUNNING'
else
    echo 'Apache2 service: NOT RUNNING'
fi
"@

Write-Info "Please enter password when prompted by SSH"
$VerifyResult = ssh "${SSHUser}@${ServerIP}" $VerifyCommands
Write-Host $VerifyResult

# Final status
Write-Success "✅ Deployment completed successfully!"
Write-Info "📁 File location: $RemotePath/index.html"
Write-Info "🌐 Domain: http://$ApacheSite"
Write-Info "📊 Local file size: $FileSizeMB KB"

Write-Warning "Note: DNS propagation may still be in progress"
Write-Info "Test locally on server: curl -H 'Host: $ApacheSite' http://localhost/"
Write-Info "Monitor DNS: dig $ApacheSite"

Write-Host ""
Write-Success "🎉 PDF to Excel Converter is now live!"