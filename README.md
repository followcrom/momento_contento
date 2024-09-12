# Momento Contento 🌟🧠

In this Flask app, a quote is chosen at random from an sqlite3 database and displayed. Users can contribute their own wisdom to the database. Accessible through a user-friendly UI.

<div style="text-align: center;">

![GitHub last commit](https://img.shields.io/github/last-commit/followcrom/Momento-Contento)

![GitHub commit activity](https://img.shields.io/github/commit-activity/m/followcrom/Momento-Contento)

![Momento Contento web interface](https://www.followcrom.online/embeds/gh_domdom_readme.jpg)
</div>

# Local Development

Start the venv:

```bash
source venv/bin/activate
```

Navigate to the app directory so the app can find the database. Run the Flask app:

```bash
flask --app application run
```

# Azure VM

Build a venv if necessary:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Flask Development Server

To make your app accessible via the VM's public IP address, you need to bind it to 0.0.0.0 instead of 127.0.0.1:

```bash
flask --app application run --host=0.0.0.0
```

The app is running on the public IP address of the VM:
http://51.140.101.98:5000/

Ensure that the port you're using is open in the Azure VM's network security group. This is not necessary when using Nginx as a reverse proxy.

## Gunicorn (Application Server)

Gunicorn acts as a WSGI (Web Server Gateway Interface) server. It ensures that the Python application can communicate with the web server and vice versa. Gunicorn is responsible for hosting your Flask application, running its Python code, and handling the application logic.

WSGI servers point directly at the Flask application object. The `if __name__ == "__main__":` block is not executed, as the server does not run the script in the same way as running it directly as a Python script. Instead, Gunicorn is executed with a gunicorn command.

### Start Gunicorn Manually

Navigate to your Flask application directory, activate your virtual environment, and start Gunicorn:

```bash
cd /home/azureuser/app
source venv/bin/activate
gunicorn --workers 3 --bind 0.0.0.0:5000 application:application
```

## Nginx (Web Server/Reverse Proxy)

Nginx acts as a reverse proxy in front of Gunicorn. This means it receives client requests and forwards them to Gunicorn. After Gunicorn processes the requests, Nginx receives the responses and forwards them back to the clients. Nginx efficiently serves static content and manages client connections, and Gunicorn executes Python application code.

Setting up Nginx as a reverse proxy to serve your Flask application through a bare IP address is a good practice.

### Install Nginx

```bash
sudo apt-get update
sudo apt-get install nginx
```

Create a new configuration file under `/etc/nginx/sites-available/`.

```bash
sudo nano /etc/nginx/sites-available/momcon
```

### Configuration

In the file, enter the following configuration, adjusting paths, server names, and ports as necessary:

```nginx
server {
    listen 80;
    server_name 51.140.101.98; # Replace with your VM's IP address.

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### Enable the Configuration

Create a symbolic link to your configuration in `/etc/nginx/sites-enabled/` to enable it.

```bash
sudo ln -s /etc/nginx/sites-available/momcon /etc/nginx/sites-enabled
```

### Test Nginx Configuration

Ensure there are no syntax errors in your Nginx configurations.

`sudo nginx -t`

### Restart Nginx

Apply the changes by restarting Nginx.

`sudo systemctl restart nginx`

### Nginx Error Logs

`sudo tail -n 10 /var/log/nginx/error.log`

## Systemd Service

To ensure your Flask app runs continuously and starts automatically at boot, you can create a systemd service for Gunicorn.

### Create a systemd service file (.service)

```bash
sudo nano /etc/systemd/system/momcon.service
```

### Service Configuration

See below for configuration details.

```ini
[Unit]
Description=Gunicorn instance to serve my momcon app
After=network.target

[Service]
User=azureuser
Group=www-data
WorkingDirectory=/home/azureuser/app
Environment="PATH=/home/azureuser/app/venv/bin"
ExecStart=/home/azureuser/app/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 application:application

[Install]
WantedBy=multi-user.target
```

### Service Configuration Details

**After:** Specifies that the service should start after the network is ready.

**User and Group:** The user and group under which Gunicorn will run. The www-data group is commonly used in web server environments. Running web server processes under a specific group like www-data is a security best practice. It limits the permissions of the process to only what's necessary for serving web content.

**WorkingDirectory:** where your Flask app is located.

**Environment:** The path to the virtual environment where Gunicorn and Flask are installed.

**ExecStart:** The command to start Gunicorn. (The equivalent of running `gunicorn --workers 3 --bind 0.0.0.0:5000 application:application`)

    - /home/azureuser/myflaskapp/venv/bin/gunicorn: This specifies the full path to the Gunicorn executable.

    - --workers 3: Tells Gunicorn to use 3 worker processes for handling requests. The common formula is `2 * number_of_cpu_cores + 1`. Since you're using a B1s Azure VM with 1 vCPU, starting with 3 workers is reasonable.

    - application:application: The application module and the application callable within that module that Gunicorn should use to run the Flask app.

### Enable and Start the Service
Reload systemd: Tell systemd to reload its configuration files, including the new service file you just created.

```bash
sudo systemctl daemon-reload

# Enable the new service so it starts automatically at boot.
sudo systemctl enable momcon.service

# Start the service immediately without waiting for a reboot.
sudo systemctl start momcon.service
```

### Commands for managing Gunicorn Service

Now we can use the .service file to manage the Gunicorn service. 

```bash
sudo systemctl restart momcon

sudo systemctl status momcon

sudo systemctl start momcon

sudo systemctl stop momcon

# Disable - prevent from starting automatically at boot
sudo systemctl disable momcon
```

## Authors

🌐 followCrom: [followcrom.online](https://followcrom.online/index.html) 🌐

📫 followCrom: [get in touch](https://followcrom.online/contact/contact.php) 📫

[![Static Badge](https://img.shields.io/badge/followcrom-.online-blue?style=for-the-badge)](http://followcrom.online)
