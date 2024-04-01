#!/bin/bash

# Install Nginx
sudo apt update
sudo apt install -y nginx

# Create Nginx configuration for the Flask app
CONFIG='/etc/nginx/sites-available/momcon'
sudo touch $CONFIG
echo 'server {
    listen 80;
    server_name 51.140.101.98;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}' | sudo tee $CONFIG

# Enable the configuration
sudo ln -s /etc/nginx/sites-available/momcon /etc/nginx/sites-enabled

# Test and restart Nginx
sudo nginx -t && sudo systemctl restart nginx
