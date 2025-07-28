#!/bin/bash

# PDF to Excel Converter - Production Deployment Script
# Usage: ./deploy.sh [server_ip] [ssh_user]

set -e  # Exit on any error

# Configuration
LOCAL_FILE="dist/index-oneliner.html"
REMOTE_PATH="/var/www/html/pdf-to-excel"
APACHE_SITE="pdf-to-excel.basangdata.com"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Parse arguments
SERVER_IP=${1:-"45.32.105.73"}
SSH_USER=${2:-"aan"}

log_info "Starting deployment to $SSH_USER@$SERVER_IP"

# Check if local file exists
if [ ! -f "$LOCAL_FILE" ]; then
    log_error "Local file $LOCAL_FILE not found!"
    log_info "Run 'npm run build' first to create the production file"
    exit 1
fi

log_success "Found local file: $LOCAL_FILE"

# Show file info
FILE_SIZE=$(ls -lh "$LOCAL_FILE" | awk '{print $5}')
log_info "File size: $FILE_SIZE"

# Test SSH connection
log_info "Testing SSH connection..."
if ! ssh -o ConnectTimeout=10 -o BatchMode=yes "$SSH_USER@$SERVER_IP" "echo 'SSH connection successful'" 2>/dev/null; then
    log_error "Cannot connect to $SSH_USER@$SERVER_IP"
    log_info "Make sure:"
    log_info "1. SSH key is added to ssh-agent"
    log_info "2. Server IP is correct"
    log_info "3. SSH user has sudo privileges"
    exit 1
fi

log_success "SSH connection successful"

# Deploy the file
log_info "Deploying $LOCAL_FILE to production server..."

# Create deployment commands
DEPLOY_COMMANDS="
set -e

# Create directory if it doesn't exist
sudo mkdir -p $REMOTE_PATH
log_info 'Created directory: $REMOTE_PATH'

# Set proper ownership
sudo chown www-data:www-data $REMOTE_PATH
log_info 'Set ownership to www-data:www-data'

# Set proper permissions
sudo chmod 755 $REMOTE_PATH
log_info 'Set directory permissions to 755'

# Enable Apache site if not already enabled
if ! sudo a2ensite $APACHE_SITE 2>/dev/null; then
    log_info 'Site already enabled or configuration not found'
else
    log_success 'Enabled Apache site: $APACHE_SITE'
fi

# Enable required Apache modules
sudo a2enmod headers rewrite
log_info 'Enabled Apache modules: headers, rewrite'

# Reload Apache configuration
sudo systemctl reload apache2
log_success 'Reloaded Apache configuration'

echo 'Server preparation complete'
"

# Execute server preparation
log_info "Preparing server..."
ssh "$SSH_USER@$SERVER_IP" "$DEPLOY_COMMANDS"

# Copy the file
log_info "Uploading file..."
scp "$LOCAL_FILE" "$SSH_USER@$SERVER_IP:/tmp/index.html"

# Move file to final location and set permissions
FINAL_SETUP="
set -e

# Move file to web directory
sudo mv /tmp/index.html $REMOTE_PATH/index.html
log_success 'Moved file to $REMOTE_PATH/index.html'

# Set proper file ownership and permissions
sudo chown www-data:www-data $REMOTE_PATH/index.html
sudo chmod 644 $REMOTE_PATH/index.html
log_success 'Set file permissions'

# Test Apache configuration
if sudo apache2ctl configtest; then
    log_success 'Apache configuration is valid'
else
    log_error 'Apache configuration has errors'
    exit 1
fi

# Final reload
sudo systemctl reload apache2
log_success 'Final Apache reload complete'

echo 'Deployment successful!'
"

ssh "$SSH_USER@$SERVER_IP" "$FINAL_SETUP"

# Verify deployment
log_info "Verifying deployment..."

VERIFY_COMMANDS="
# Check if file exists and get info
if [ -f '$REMOTE_PATH/index.html' ]; then
    FILE_SIZE=\$(ls -lh '$REMOTE_PATH/index.html' | awk '{print \$5}')
    FILE_OWNER=\$(ls -l '$REMOTE_PATH/index.html' | awk '{print \$3\":\" \$4}')
    echo \"File deployed: \$FILE_SIZE, Owner: \$FILE_OWNER\"
else
    echo 'ERROR: File not found at $REMOTE_PATH/index.html'
    exit 1
fi

# Test local HTTP response
HTTP_STATUS=\$(curl -s -o /dev/null -w '%{http_code}' -H 'Host: $APACHE_SITE' http://localhost/ || echo 'FAILED')
echo \"Local HTTP test: \$HTTP_STATUS\"

# Check Apache status
if systemctl is-active --quiet apache2; then
    echo 'Apache2 service: RUNNING'
else
    echo 'Apache2 service: NOT RUNNING'
fi
"

VERIFY_RESULT=$(ssh "$SSH_USER@$SERVER_IP" "$VERIFY_COMMANDS")
echo "$VERIFY_RESULT"

# Final status
log_success "✅ Deployment completed successfully!"
log_info "📁 File location: $REMOTE_PATH/index.html"
log_info "🌐 Domain: http://$APACHE_SITE"
log_info "📊 Local file size: $FILE_SIZE"

log_warning "Note: DNS propagation may still be in progress"
log_info "Test locally on server: curl -H 'Host: $APACHE_SITE' http://localhost/"
log_info "Monitor DNS: dig $APACHE_SITE"

echo
log_success "🎉 PDF to Excel Converter is now live!"