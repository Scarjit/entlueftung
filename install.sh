#!/usr/bin/env sh

# Check for root
if [ "$(id -u)" -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

# Copy entlueftung.service to systemd directory
cp entlueftung.service /etc/systemd/system/

# Reload systemd
systemctl daemon-reload

# Enable entlueftung service
systemctl enable entlueftung.service

# Start entlueftung service
systemctl start entlueftung.service