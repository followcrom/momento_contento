from flask import Flask, render_template, jsonify, request, url_for
from database import load_domdoms_from_db, load_domdom_from_db, add_to_db
import random

application = Flask(__name__)

# Set the application root for subpath support
application.config['APPLICATION_ROOT'] = '/momcon'

# Create a function to generate URLs with the correct subpath
def url_for_with_subpath(endpoint, **values):
    # Generate the URL using url_for
    url = url_for(endpoint, **values)
    # Add the application root if it isn't already present
    # if not url.startswith(application.config['APPLICATION_ROOT']):
    #     url = application.config['APPLICATION_ROOT'] + url
    return url

# Add the function to Jinja2 environment
application.jinja_env.globals['url_for_with_subpath'] = url_for_with_subpath

@application.route("/")
def show_dom():
    domdoms = load_domdoms_from_db()
    numdoms = len(domdoms)
    id_range = [d["id"] for d in domdoms]
    dom_id = random.choice(id_range)
    domdom = load_domdom_from_db(dom_id)
    return render_template("index.html", domdom=domdom, dom_id=dom_id, numdoms=numdoms)

@application.route("/api")
def show_json():
    domdoms = load_domdoms_from_db()
    return jsonify(domdoms)

@application.route("/sent", methods=["POST"])
def send_wisdom():
    data = request.form
    add_to_db(data)
    return render_template("submitted.html", submission=data)

if __name__ == "__main__":
    application.run(debug=True)


# if __name__ == "__main__":
#     application.run(debug=True)


# # Specifically used to run on Flask's built-in development server:
# if __name__ == "__main__":
#     application.run(port=5000)
