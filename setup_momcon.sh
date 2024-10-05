#!/bin/bash

# Set up logging
LOGFILE="/var/log/momcon_setup.log"
exec > >(tee -a "$LOGFILE") 2>&1

echo "Starting setup script at $(date)"

# Navigate to the app directory
cd /var/www/momcon || { echo "Directory /var/www/momcon not found."; exit 1; }

# Set up Python virtual environment
python3 -m venv .momcon_venv
source .momcon_venv/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create Nginx configuration for the app
cat > /etc/nginx/sites-available/momcon <<EOF
server {
    server_name followcrom.com www.followcrom.com;

    location /momcon/ {
        proxy_pass http://localhost:5000/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /static/ {
        alias /var/www/momcon/static/;
    }
}
EOF

# Enable the Nginx site configuration by creating a symbolic link if it doesn't exist
if [ ! -L /etc/nginx/sites-enabled/momcon ]; then
    ln -s /etc/nginx/sites-available/momcon /etc/nginx/sites-enabled/momcon
fi

# Test Nginx configuration for syntax errors
if nginx -t; then
    echo "Nginx configuration syntax is okay."
    systemctl restart nginx
    echo "Nginx restarted successfully."
else
    echo "Error in Nginx configuration." >&2
    exit 1
fi

# Create systemd service for the app
cat > /etc/systemd/system/momcon.service <<EOF
[Unit]
Description=Gunicorn instance to serve Momento Contento app
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/momcon
Environment="PATH=/var/www/momcon/.momcon_venv/bin"
Environment="FLASK_ENV=production"
Environment="AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY_ID"
Environment="AWS_SECRET_ACCESS_KEY=YOUR_SECRET_ACCESS_KEY"
Environment="AWS_DEFAULT_REGION=eu-west-2"
ExecStart=/var/www/momcon/.momcon_venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 application:application

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd to apply changes and enable/start the service
systemctl daemon-reload
systemctl enable momcon
systemctl start momcon

# Optionally restart the service to ensure it's running
systemctl restart momcon

echo "Setup complete. Your application should be accessible at http://followcrom.com/momcon/"
