from flask import Flask, redirect, render_template, request, url_for

import helpers
import os
import sys
from analyzer import Analyzer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():

    # validate screen_name
    screen_name = request.args.get("screen_name", "")
    if not screen_name:
        return redirect(url_for("index"))

    # path to positive and negative word dictionary
    positives = os.path.join(sys.path[0], "positive-words.txt")
    negatives = os.path.join(sys.path[0], "negative-words.txt")

    # get screen_name's tweets
    tweets = helpers.get_user_timeline(screen_name)
    if tweets == None:
        return render_template("index.html")

    #initialize analyzer
    analyzer = Analyzer(positives, negatives)

    cpositive, cnegative, cneutral = 0.0, 0.0, 0.0
    for tweet in tweets:
        #give a score to every tweet
        score = analyzer.analyze(tweet)
        if score > 0.0:
           cpositive += 1
        elif score < 0.0:
            cnegative += 1
        else:
            cneutral +=1

    total = cpositive + cnegative +cneutral
    if total == 0:
        return render_template("index.html")

    positive, negative, neutral = cpositive/total, cnegative/total, cneutral/total

    # generate chart
    chart = helpers.chart(positive, negative, neutral)

    # render results
    return render_template("search.html", chart=chart, screen_name=screen_name)


