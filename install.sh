#!/bin/bash

# Variables - Adjust these as needed
APP_NAME="myapp"
APP_DIR="/path/to/your/flask/app"
NGINX_CONF="$APP_DIR/nginx/$APP_NAME.conf"       # Path to your nginx config file
SYSTEMD_SERVICE="$APP_DIR/systemd/$APP_NAME.service" # Path to your systemd service file
VENV_DIR="$APP_DIR/venv"                        # Path to your virtual environment
SOCKET_FILE="$APP_DIR/$APP_NAME.sock"

# Function to check for superuser privileges
check_sudo() {
    if [[ "$EUID" -ne 0 ]]; then
        echo "Please run as root or with sudo"
        exit 1
    fi
}

# Function to install necessary dependencies
install_dependencies() {
    echo "Installing necessary dependencies..."
    dnf update
    dnf install -y nginx python3-venv python3-pip
}

# Function to set up virtual environment
setup_virtualenv() {
    echo "Setting up virtual environment..."
    if [ ! -d "$VENV_DIR" ]; then
        python3 -m venv "$VENV_DIR"
    fi
    "$VENV_DIR/bin/pip" install --upgrade pip
    "$VENV_DIR/bin/pip" install -r "$APP_DIR/requirements.txt"
}

# Function to copy Nginx configuration
setup_nginx() {
    echo "Setting up Nginx configuration..."
    if [ -f "$NGINX_CONF" ]; then
        cp "$NGINX_CONF" "/etc/nginx/conf.d/"
        nginx -t && systemctl reload nginx
        echo "Nginx configuration applied and reloaded."
    else
        echo "Nginx configuration file not found: $NGINX_CONF"
        exit 1
    fi
}

# Function to set up systemd service
setup_systemd() {
    echo "Setting up systemd service..."
    if [ -f "$SYSTEMD_SERVICE" ]; then
        cp "$SYSTEMD_SERVICE" "/etc/systemd/system/$APP_NAME.service"
        systemctl daemon-reload
        systemctl enable "$APP_NAME.service"
        systemctl start "$APP_NAME.service"
        echo "Systemd service started and enabled."
    else
        echo "Systemd service file not found: $SYSTEMD_SERVICE"
        exit 1
    fi
}

# Function to adjust file permissions
adjust_permissions() {
    echo "Adjusting file permissions..."
    chown -R www-data:www-data "$APP_DIR"
    chmod -R 755 "$APP_DIR"
    chmod 664 "/etc/systemd/system/$APP_NAME.service"
    echo "Permissions set."
}

# Main script execution
check_sudo
install_dependencies
setup_virtualenv
setup_nginx
setup_systemd
adjust_permissions

echo "Installation and setup complete."
