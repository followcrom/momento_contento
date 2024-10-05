from flask import Flask, render_template, jsonify, request, url_for
from database import load_domdoms_from_db, load_domdom_from_db, add_to_db
import random
import subprocess
import os
from flask import request
import datetime

application = Flask(__name__)

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

@application.route("/momcon/")
def show_dom():
    domdoms = load_domdoms_from_db()
    numdoms = len(domdoms)
    id_range = [d["id"] for d in domdoms]
    dom_id = random.choice(id_range)
    domdom = load_domdom_from_db(dom_id)
    return render_template("index.html", domdom=domdom, dom_id=dom_id, numdoms=numdoms)

@application.route("/momcon/api")
def show_json():
    domdoms = load_domdoms_from_db()
    return jsonify(domdoms)

@application.route("/momcon/sent", methods=["POST"])
def send_wisdom():
    data = request.form
    add_to_db(data)

    # Send an SNS alert using AWS CLI via subprocess
    message = (
    "A new moment has been added to the database.\n\n"
    "Details:\n"
    f"Title: {data['title']}\n"
    f"Wisdom: {data['wisdom']}\n"
    f"Submitted at: {datetime.datetime.now().isoformat()}\n\n"
    "Check the site for more information."
)
    topic_arn = "arn:aws:sns:eu-west-2:131936741611:momcon"

    # Command to publish SNS notification
    command = [
        "/usr/bin/aws", "sns", "publish",
        "--topic-arn", topic_arn,
        "--message", message,
        "--subject", "New MomCon added to DB"
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error sending SNS message: {e}")
    
    return render_template("submitted.html", submission=data)
