import os
import re
from flask import redirect, Flask, jsonify, render_template, request, url_for
from flask_jsglue import JSGlue
import feedparser

from cs50 import SQL
from helpers import lookup

# configure application
app = Flask(__name__)
JSGlue(app)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///events.db")

#landing page
@app.route("/", methods=["GET", "POST"] )
def landing():
    """Render map."""
    # if method is POST (through clicking the submit button), we want to execute something to the database
    if request.method == "POST":
        # check if input is given (TODO! javascript checking as well)
        if request.form.get('rating'):
            rate = int(request.form.get('rating'))
        else:
            return "No input given"

        # update the database with the new value of average_rate and rated
        db.execute("INSERT INTO reviews VALUES(NULL, :organization_id, :rate, :review)", organization_id = request.form.get('submitValue'), rate = request.form.get('rating'), review = request.form.get('review'))

        # reload the page
        return render_template("landing.html")
    # if method == GET, return landing
    else:
        return render_template("landing.html")

#
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form.get("name")
        street_num = request.form.get("street_num")
        route = request.form.get("route")
        city = request.form.get("city")
        country = request.form.get("country")
        website = request.form.get("website")
        # checks are alse excecuted backend if Javascript frontend fails
        if not name:
            return "please enter your name!"
        if not city:
            return "please enter your city!"
        if not country:
            return "please enter your country!"
        #TODO check values for website, other checks, Javascript for doing the error checks?

        # Insert values in database
        db.execute("INSERT INTO organization VALUES (NULL, :name, :city, :country, :website)", name=name, city=city,country=country,website=website)
        return redirect(url_for("landing"))
    else:
        return render_template("add.html")

# this route keeps track of the organizations in JSON
@app.route("/organization", methods=["GET"])
def organization():
    # if request via GET shows organization_id, we only want to show the organizations which match this id
    if request.args.get('organization_id'):
        organization_id = request.args.get('organization_id')
        data = db.execute("SELECT * FROM organization WHERE organization.organization_id = :organization_id", organization_id = organization_id)
        return jsonify(data)
    else:
        return jsonify(db.execute("SELECT * FROM organization"))

@app.route("/review", methods=["GET"])
def review():
    organization_id = request.args.get('organization_id')
    data = db.execute("SELECT * FROM reviews WHERE reviews.organization_id =:organization_id", organization_id = organization_id)
    return jsonify(data)


#TODO!
@app.route("/event", methods=["GET"])
def event():
    return jsonify(db.execute("SELECT * from event"))


