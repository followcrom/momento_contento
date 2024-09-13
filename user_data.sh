#!/bin/bash

# Variables
APP_DIR="/var/www/momento_contento"
REPO_URL="https://github.com/followcrom/momento_contento.git"
GUNICORN_PORT="5000"

# Create application directory if it doesn't exist
if [ ! -d "$APP_DIR" ]; then
    mkdir -p "$APP_DIR"
fi

# Clone the Flask app's Git repository
if [ -d "$APP_DIR/.git" ]; then
    echo "Repository already exists, pulling latest changes..."
    cd "$APP_DIR"
    git pull
else
    echo "Cloning repository..."
    git clone "$GIT_REPO" "$APP_DIR"
    cd "$APP_DIR"
fi

cd "$APP_DIR/app"

# Set up Python virtual environment
python3 -m venv momcon_venv
source momcon_venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create Nginx configuration for the app
bash -c "cat > /etc/nginx/sites-available/momcon" <<EOF
server {
    listen 80;
    server_name 188.166.155.230;

    location /momcon/ {
        proxy_pass http://localhost:5000/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
}
EOF

# Enable the Nginx site
ln -sf /etc/nginx/sites-available/momcon /etc/nginx/sites-enabled

# Test Nginx configuration and restart
nginx -t && systemctl restart nginx

# Create Systemd service for Gunicorn
bash -c "cat > /etc/systemd/system/momcon.service" <<EOF
[Unit]
Description=Gunicorn instance to serve Momento Contento app
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=$APP_DIR/app
Environment="PATH=$APP_DIR/app/momcon_venv/bin"
ExecStart=$APP_DIR/app/momcon_venv/bin/gunicorn --workers 3 --bind 0.0.0.0:$GUNICORN_PORT application:application

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd, enable and start the Gunicorn service
systemctl daemon-reload
systemctl enable momcon
systemctl start momcon
