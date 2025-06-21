# MomCon on the D.O. Box ˖°𓇼🌊⋆🐚🫧

## Check Disk Usage 💾

```bash
df -h
```

The `df` command shows the amount of disk space used and available on all mounted filesystems. The `-h` option makes the output "human-readable," displaying sizes in GB, MB, etc.

### ⬅️ Before `git cloning` **momcon**:

```bash
/dev/vda1 (Main disk):
Size: 25 GB total disk space.
Used: 3.9 GB is used.
Avail: 21 GB is available.
Use%: 17% of the disk space is used.
```

#### ➡️ After

```bash
/dev/vda1
Size: 25 GB total disk space.
Used: 4.0 GB is used.
Avail: 21 GB is available.
Use%: 17% of the disk space is used.
```

## Reading from the DB 🛢️
To read from the SQLite database, you can use the `sqlite3` command-line tool. Below is an example of how to connect to the `momcons.db` database, list the tables, and query the `momcons` table.

```bash
cd /var/www/momcon

sqlite3 momcons.db

.tables

SELECT * FROM momcons;

DELETE FROM momcons WHERE id = 16;

.quit
```

## 📜 User Data 📝

```sh
#!/bin/bash

# Set up logging
LOGFILE="/var/log/momcon_setup.log"
exec > >(tee -a "$LOGFILE") 2>&1

echo "Starting setup script at $(date)"

# Update package lists
sudo apt update -y

# Upgrade packages non-interactively, automatically handle prompts
sudo DEBIAN_FRONTEND=noninteractive apt-get upgrade -y

# Install packages. curl is needed to fetch the public IP address
sudo apt install -y python3-pip python3-venv nginx git curl

# Restart and enable Nginx to run on startup
sudo systemctl restart nginx
sudo systemctl enable nginx

# Variables
APP_DIR="/var/www/momento_contento"
REPO_URL="https://github.com/followcrom/momento_contento.git"
GUNICORN_PORT="5000"

# Create application directory if it doesn't exist
if [ ! -d "$APP_DIR" ]; then
    mkdir -p "$APP_DIR"
fi

# Clone the Git repository
if [ -d "$APP_DIR/.git" ]; then
    echo "Repository already exists, pulling latest changes..."
    cd "$APP_DIR"
    git pull
else
    echo "Cloning repository..."
    git clone "$REPO_URL" "$APP_DIR"
    cd "$APP_DIR"
fi

cd "$APP_DIR/app"

# Set up Python virtual environment
python3 -m venv .momcon_venv
source .momcon_venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# To detect the public IP address of a VM on Digital Ocean
PUBLIC_IP=$(curl -s http://169.254.169.254/metadata/v1/interfaces/public/0/ipv4/address)

# To detect the public IP address of the VM using the AWS EC2 metadata service
# PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)

# Create Nginx configuration for the app
# Be sure to use Escaped Dollar Signs ($host, $remote_addr, etc.) to prevent shell interpretation errors
sudo bash -c "cat > /etc/nginx/sites-available/momcon" <<EOF
server {
    listen 80;
    server_name $PUBLIC_IP;

    # Flask app under /momcon. Be sure to adjust Flask for subpath
    location /momcon/ {
        proxy_pass http://localhost:5000/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /static/ {
        alias /var/www/momento_contento/app/static/;
    }
}
EOF

# Enable the Nginx site
sudo ln -sf /etc/nginx/sites-available/momcon /etc/nginx/sites-enabled

# Test Nginx configuration for syntax errors
if sudo nginx -t; then
    echo "Nginx configuration syntax is okay."
    sudo systemctl restart nginx
    echo "Nginx restarted successfully."
else
    echo "Error in Nginx configuration."
fi

# Create Systemd service for Gunicorn
# Use cat (or tee) to write the content directly. Using nano requires user interaction
sudo bash -c "cat > /etc/systemd/system/momcon.service" <<EOF
[Unit]
Description=Gunicorn instance to serve Momento Contento app
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=$APP_DIR/app
Environment="PATH=$APP_DIR/app/momcon_venv/bin"
Environment="FLASK_ENV=production"
Environment="AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY_ID"
Environment="AWS_SECRET_ACCESS_KEY=YOUR_SECRET_ACCESS_KEY"
Environment="AWS_DEFAULT_REGION=eu-west-2"
ExecStart=$APP_DIR/app/momcon_venv/bin/gunicorn --workers 3 --bind 0.0.0.0:$GUNICORN_PORT application:application

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd, enable and start the Gunicorn service
sudo systemctl daemon-reload
sudo systemctl enable momcon
sudo systemctl start momcon
sudo systemctl restart momcon

echo "Setup complete. Your application should be accessible at http://$PUBLIC_IP/momcon/"
```


## Use Environment Variables

You can use environment variables to differentiate between your local and production environments. This way, you can set the static folder and URL path according to the environment.

```bash
# For local development
export FLASK_ENV=development

# For production, this needs to be set in the momcon systemd service
Environment="FLASK_ENV=production"
```

**NOTE**: services started by `systemd` do not inherit environment variables from the user’s shell environment. Explicitly setting them in the service file is one way to ensure the app can access them. Another approach is to use a `.env` file and load them programmatically in the application.

### Set local FLASK_ENV Permanently

```bash
nano ~/.bashrc

# Add the following line to set FLASK_ENV:
export FLASK_ENV=development

# Save the file and run:
source ~/.bashrc

# Check the Current FLASK_ENV Value
echo $FLASK_ENV
```

## 🛤️ Adjust Flask for Subpath 🏞

#### `application.py`

```python
# Check if 'FLASK_ENV' is set in the environment
env = os.getenv('FLASK_ENV', 'development')  # Defaults to 'development' if FLASK_ENV is not set

if env == 'development':
    print('FLASK_ENV environment variable not set. Defaulting to development.')

print(f"Current environment: {os.environ.get('FLASK_ENV')}")

# Set static folder and URL path based on the environment
if env == 'production':
    application = Flask(__name__, static_url_path='/momcon/static', static_folder='/var/www/momcon/static')
    application.config['APPLICATION_ROOT'] = '/momcon'  # Production app root
else:
    application = Flask(__name__, static_folder='static')
    application.config['APPLICATION_ROOT'] = '/'  # Local app root

# Create a function to generate URLs with the correct subpath
def url_for_with_subpath(endpoint, **values):
    # Generate the URL using url_for
    url = url_for(endpoint, **values)
    
    # Add the application root if running in production
    if env == 'production':
        if not url.startswith(application.config['APPLICATION_ROOT']):
            url = application.config['APPLICATION_ROOT'] + url
    else:
        # Adjust for local development, account for '/momcon' being part of the URL
        if 'momcon' not in request.url_root and not url.startswith('/momcon'):
            url = "/momcon" + url

    return url

# Add the function to Jinja2 environment
application.jinja_env.globals['url_for_with_subpath'] = url_for_with_subpath
```

#### `form.html`

```html
<form action="{{ url_for_with_subpath('send_wisdom') }}" method="post">
```

<br>

# 💫 Upload Changes and Restart

```bash
git pull
systemctl restart momcon
```

<br>

# Troubleshooting 👨‍🔧

`journalctl -u momcon -n 20`

```bash
systemctl status momcon
systemctl restart momcon
```

Test that the app is running correctly by accessing it directly on port 5000 before involving Nginx:

```bash
curl http://localhost:5000/
```

### Permissions 🧙🏼‍♂️

Make sure that the user running Gunicorn has the proper permissions for the app directory. If needed, change file ownership:

```bash
sudo chown -R root:www-data /var/www/momento_contento
```

### Considerations 🤔

**Firewall Settings**: Ensure that port 5000 is open on the DigitalOcean VM.

```bash
sudo ufw allow 5000
sudo ufw reload
sudo ufw status
```

# Logs 🪵

```bash
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

## Gunicorn Logs 🦄

```bash
journalctl -u momcon -n 20
journalctl -u momcon
# or
sudo journalctl -u momcon.service
```
