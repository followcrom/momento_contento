from flask import Flask, render_template, jsonify, request
from sqlalchemy import text
from database import engine, load_domdoms_from_db, load_domdom_from_db, add_to_db
import random

application = Flask(__name__)


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


@application.route("/sent", methods=["post"])
def send_wisdom():
    data = request.form
    add_to_db(data)
    return render_template("submitted.html", submission=data)


if __name__ == "__main__":
    application.run()
