import os
import re
from flask import Flask, jsonify, render_template, request, url_for
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
db = SQL("sqlite:///mashup.db")

@app.route("/")
def index():
    """Render map."""
    if not os.environ.get("API_KEY"):
        raise RuntimeError("API_KEY not set")
    return render_template("index.html", key=os.environ.get("API_KEY"))

@app.route("/articles")
def articles():
    """Look up articles for geo."""

    # retrieve geo argument from HTML form
    geo = request.args.get("geo")

    # if argument is missing, raise RuntimeError
    if not geo:
        raise RuntimeError("Geo not set")

    # search for articles in that geo
    articles = lookup(geo)

    # return up to 5 articles as a JSON object
    if len(articles) > 5:
        return jsonify([articles[0], articles[1], articles[2], articles[4], articles[5]])
    else:
        return jsonify(articles)

@app.route("/search")
def search():
    """Search for places that match query."""

    # get q from the GET request
    q = request.args.get("q")

    arguments = []
    # convert q to a list of alphanumerical strings
    while not q.isalnum():
        if q[0].isalnum():
            # iterate over string till non alnum is found
            for i in range(len(q)):
                if not q[i].isalnum():
                    start = i
                    # add string to arguments which starts with alnum and ends with non alnum to arguments
                    arguments.append('%' + q[:start] + '%')
                    break
            # skip non alnum characters
            while(not q[start].isalnum()):
                # to handle the case if q ends witn non alnum
                if(len(q[start:]) == 1):
                    break
                start += 1
            # asign new value to q
            q = q[start:]
        # to handle the case if q starts with non alnum
        else:
            # to handle the case if q ends with non alnum
            if len(q) == 1:
                break
            q = q[1:]
    # add string to arguments which ends with the end of q
    if q.isalnum():
        arguments.append('%' + q +'%')

    # Create a SQL querry with a length depending on the amount of arguments
    i = 0
    string = "SELECT * FROM places WHERE("
    while i < len(arguments):
        string = string+"country_code LIKE :q"+str(i)+" OR postal_code LIKE :q"+str(i)+" OR place_name LIKE :q"+str(i)+" OR admin_name1 LIKE :q"+str(i)+" OR admin_code1 LIKE :q"+str(i)+" OR admin_name2 LIKE :q"+str(i)+" OR admin_code2 LIKE :q"+str(i)+" OR admin_name3 LIKE :q"+str(i)+" OR admin_code3 LIKE :q"+str(i)+" OR latitude LIKE :q"+str(i)+" OR longitude LIKE :q"+str(i)
        test ="test"
        # add AND condition
        if not i == len(arguments)-1:
            string = string+") AND ("
        i += 1
    # End the Query
    string = string + ')'

    # run the querry
    if len(arguments) ==1:
        result = db.execute(string, q0=arguments[0])
    elif len(arguments) ==2:
        result = db.execute(string, q0=arguments[0], q1 = arguments[1])
    elif len(arguments) ==3:
        result = db.execute(string, q0=arguments[0], q1 = arguments[1], q2 = arguments[2])
    elif len(arguments) ==4:
        result = db.execute(string, q0=arguments[0], q1 = arguments[1], q2 = arguments[2], q3 =arguments[3])
    elif len(arguments) ==5:
        result = db.execute(string, q0=arguments[0], q1 = arguments[1], q2 = arguments[2], q3 = arguments[3], q4 = arguments[4])
    else:
        result = db.execute(string, q0=arguments[0], q1 = arguments[1], q2 = arguments[2], q3 = arguments[3], q4 = arguments[4], q5 = arguments[5])

    # return the result as a JSON
    return jsonify(result)

@app.route("/update")
def update():
    """Find up to 10 places within view."""

    # ensure parameters are present
    if not request.args.get("sw"):
        raise RuntimeError("missing sw")
    if not request.args.get("ne"):
        raise RuntimeError("missing ne")

    # ensure parameters are in lat,lng format
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("sw")):
        raise RuntimeError("invalid sw")
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("ne")):
        raise RuntimeError("invalid ne")

    # explode southwest corner into two variables
    (sw_lat, sw_lng) = [float(s) for s in request.args.get("sw").split(",")]

    # explode northeast corner into two variables
    (ne_lat, ne_lng) = [float(s) for s in request.args.get("ne").split(",")]

    # find 10 cities within view, pseudorandomly chosen if more within view
    if (sw_lng <= ne_lng):

        # doesn't cross the antimeridian
        rows = db.execute("""SELECT * FROM places
            WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude AND longitude <= :ne_lng)
            GROUP BY country_code, place_name, admin_code1
            ORDER BY RANDOM()
            LIMIT 10""",
            sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    else:

        # crosses the antimeridian
        rows = db.execute("""SELECT * FROM places
            WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude OR longitude <= :ne_lng)
            GROUP BY country_code, place_name, admin_code1
            ORDER BY RANDOM()
            LIMIT 10""",
            sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    # output places as JSON
    return jsonify(rows)
