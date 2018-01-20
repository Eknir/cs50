from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    # select all stocks which were bought
    bought = db.execute("SELECT symbol, amount FROM orderbook JOIN portfolio WHERE portfolio.id == :id AND orderbook.ordertype == 'BUY' AND portfolio.order_num == orderbook.order_num", id = session["user_id"])
    # select all stocks which were sold
    sold = db.execute("SELECT symbol, amount FROM orderbook JOIN portfolio WHERE portfolio.id = :id AND orderbook.ordertype = 'SELL' AND portfolio.order_num == orderbook.order_num", id = session["user_id"])

    # initialize values
    holdings_symbol = []
    holdings_amount =[]
    holdings_price = []
    holdings_value =[]
    total_stock_value = 0
    cash = db.execute("SELECT cash FROM users WHERE id == :id", id = session["user_id"])[0] ['cash']

    # iterate over bought and fill the lists holdings_symbol, holdings_amount, holdings_price
    for purchase in bought:
        if not purchase['symbol'] in holdings_symbol:
            price = lookup(purchase['symbol']) ['price']
            holdings_symbol.append(purchase['symbol'])
            holdings_amount.append(purchase['amount'])
            holdings_price.append(price)
        else:
            for i in range(len(holdings_symbol)):
                if holdings_symbol[i] == purchase['symbol']:
                    holdings_amount[i] += purchase['amount']

    for sale in sold:
        for i in range(len(holdings_symbol)):
                if holdings_symbol[i] == sale['symbol']:
                    holdings_amount[i] -= sale['amount']
                if holdings_amount[i] == 0:
                        holdings_symbol.remove(holdings_symbol[i])
                        holdings_amount.remove(0)

    # calculate the total worth of every postion and total worth of all stocks
    for i in range(len(holdings_symbol)):
        holdings_value.append(holdings_amount[i]*holdings_price[i])
        total_stock_value += holdings_value[i]
        # format holdings_price
        holdings_price[i] = usd(holdings_price[i])
        # format holdings value
        holdings_value[i] = usd(holdings_value[i])

    # calculate the portfolio value
    portfolio_value = usd(total_stock_value + cash)
    # format cash
    cash = usd(cash)
    # formal total_stock_value
    total_stock_value = usd(total_stock_value)
    # return values to HTML template
    return render_template("index.html", cash = cash, total_stock_value = total_stock_value, portfolio_value = portfolio_value, holdings_symbol = holdings_symbol, holdings_amount = holdings_amount, holdings_price = holdings_price, holdings_value = holdings_value, length = len(holdings_symbol))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    if request.method == "POST":
        amount = request.form.get("amount")
        symbol = request.form.get("symbol")
        quote = lookup(symbol)
        # to verify that the user entered a symbol
        if not symbol:
            return apology("enter symbol")
        # to verify that the user entered an amount
        if not amount:
            return apology("enter amount")
        # to verify that the user gives an integer for amount
        if not amount.isdigit():
            return apology("Give an integer for Amount")
        # to verify that the user entered a positive amount
        if not int(amount) > 0:
            return apology("Not a valid amount")
        # to verify that the entered symbol exists
        if not quote:
            return apology("Not a valid symbol")
        # load the users cash balance
        cash = int(db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"] )[0]['cash'])
        # reject order if the user does not have enough cash
        if not cash >= int(amount) * int(quote['price']):
            return apology("not enough cash!!")
        else:
            # create an order number which corresponds to the user id
            db.execute("INSERT INTO portfolio VALUES (:id, NULL)", id = session["user_id"])
            # find the latest order number (for inserting in the orderbook)
            order_num = db.execute("SELECT order_num FROM portfolio where id = :id ORDER BY order_num DESC", id = session["user_id"])[0]['order_num']
            # insert the order in the orderbook
            db.execute("INSERT INTO orderbook VALUES (:order_num, :symbol, :amount, :price, CURRENT_TIMESTAMP, :ordertype)", order_num = order_num, symbol = symbol.upper(), amount = amount, price = quote['price'], ordertype = "BUY")
            # update the users cash balance in the database
            db.execute("UPDATE users set cash = :cash - :amount * :price WHERE id = :id", cash = cash, amount = int(amount),  price = quote['price'], id = session["user_id"])

            return redirect(url_for("index"))
    else:
        # else if user reached route via GET (as by clicking a link or via redirect)
        return render_template("buy.html")

@app.route("/history",  methods=["GET", "POST"])
@login_required
def history():
    """Show history of transactions."""
    # If the user arrives on the page by clicking a link
    if request.method == "GET":
        history = db.execute("SELECT ordertype, symbol, price, amount, timestamp from orderbook, portfolio WHERE orderbook.order_num = portfolio.order_num and portfolio.id = :id", id = session["user_id"])
        ordertype = []
        symbol = []
        amount = []
        timestamp = []
        price = []
        for i in range(len(history)):
            ordertype.append(history[i]['ordertype'])
            symbol.append(history[i]['symbol'].upper())
            amount.append(history[i]['amount'])
            timestamp.append(history[i]['timestamp'])
            price.append(usd(history[i]['price']))


        #return render_template("test.html", history = len(history))
        return render_template("history.html", ordertype = ordertype, symbol = symbol, amount = amount, timestamp = timestamp, length = len(history), price = price)
        # if the user arrives at the page via a form on the page
    else:
        symbol = request.form.get("symbol").upper()
        quote = lookup(symbol)
        # to verify that the user entered a symbol
        if not request.form.get("symbol"):
            return apology("Enter symbol")
        # to verfiy that the entered symbol exists
        if not quote:
            return apology("Not a valid symbol")

        #return render_template("test.html", symbol = symbol)
        history = db.execute("SELECT ordertype, symbol, price, amount, timestamp from orderbook, portfolio WHERE orderbook.order_num = portfolio.order_num and portfolio.id = :id and orderbook.symbol = :symbol", id = session["user_id"], symbol = symbol)
        #return render_template("test.html", symbol = history[0]["symbol"])
        ordertype = []
        symbol = []
        amount = []
        timestamp = []
        price = []
        for i in range(len(history)):
            if history[i]['symbol'] == request.form.get("symbol").upper():
                ordertype.append(history[i]['ordertype'])
                symbol.append(history[i]['symbol'].upper())
                amount.append(history[i]['amount'])
                timestamp.append(history[i]['timestamp'])
                price.append(usd(history[i]['price']))
        return render_template("history.html", ordertype = ordertype, symbol = symbol, amount = amount, timestamp = timestamp, length = len(history), price = price)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""
    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        quote = lookup(symbol)
        # to verify that the user entered a symbol
        if not request.form.get("symbol"):
            return apology("Enter symbol")
        # to verfiy that the entered symbol exists
        if not quote:
            return apology("Not a valid symbol")
        # display a template with symbol, price and name
        return render_template("quoted.html", symbol = quote['symbol'], name = quote['name'], price = usd(quote['price']))
    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        #check if user input a username
        if not request.form.get("username"):
            return apology("Missing username!")
        #check if password is not blank
        if not request.form.get("password"):
            return apology("Missing password")
         # check if user inputs two matching passwords
        if request.form.get("password") != request.form.get("cpassword"):
            return apology("Passwords did not match")
        # add user to database
        result = db.execute("INSERT INTO users VALUES (NULL, :username, :hash, 10000)", username = request.form.get('username'), hash = pwd_context.hash(request.form.get('password')))
        # check if user is not already in the database
        if not result:
            return apology("Username exists already")
        # do something with session[]
        else:
            # log in automatically
            session["user_id"] = result
            # redirect user to home page
            return redirect(url_for("index"))
    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """sell shares of stock."""
    if request.method == "POST":
        amount = request.form.get("amount")
        symbol = request.form.get("symbol")
        quote = lookup(symbol)
        # to verify that the user entered a symbol
        if not symbol:
            return apology("enter symbol")
        # to verify that the user entered an amount
        if not amount:
            return apology("enter amount")
        # to verify that the user gives an integer for amount
        if not amount.isdigit():
            return apology("Give an integer for Amount")
        # to verify that the user entered a positive amount
        if not int(amount) > 0:
            return apology("Not a valid amount")
        # to verify that the entered symbol exists
        if not quote:
            return apology("Not a valid symbol")
        # load the users cash balance

        # get all the stocks which were bought by the person
        bought = db.execute("SELECT symbol, amount FROM orderbook JOIN portfolio WHERE portfolio.id == :id AND orderbook.ordertype == 'BUY' AND portfolio.order_num == orderbook.order_num", id = session["user_id"])

        # select all stocks which were sold
        sold = db.execute("SELECT symbol, amount FROM orderbook JOIN portfolio WHERE portfolio.id = :id AND orderbook.ordertype = 'SELL' AND portfolio.order_num == orderbook.order_num", id = session["user_id"])

        # initialize values
        holdings_amount = []
        holdings_symbol = []
        cash = db.execute("SELECT cash FROM users WHERE id == :id", id = session["user_id"])[0] ['cash']

        # iterate over bought and fill the lists holdings_symbol, holdings_amount
        # TODO! Make this more efficient, because we don't have to create a full array, we only need to know the amount of the stock which needs to be sold
        for purchase in bought:
            if not purchase['symbol'] in holdings_symbol:
                holdings_symbol.append(purchase['symbol'])
                holdings_amount.append(purchase['amount'])
            else:
                for i in range(len(holdings_symbol)):
                    if holdings_symbol[i] == purchase['symbol']:
                        holdings_amount[i] += purchase['amount']
                    if holdings_amount[i] == 0:
                        holdings_symbol.remove(holdings_symbol[i])
                        holdings_amount.remove(0)

        # iterate over sold and update the lists holdings_symbol, holdings_amount
        for sale in sold:
            for i in range(len(holdings_symbol)):
                if holdings_symbol[i] == sale['symbol']:
                    holdings_amount[i] -= sale['amount']
                if holdings_amount[i] == 0:
                    holdings_symbol.remove(holdings_symbol[i])
                    holdings_amount.remove(0)

        for i in range(len(holdings_amount)):
            if holdings_symbol[i] == symbol:
                if int(amount) > int(holdings_amount[i]):
                    return apology("Not possible to sell more than you own")
        else:
            # create an order number which corresponds to the user id
            db.execute("INSERT INTO portfolio VALUES (:id, NULL)", id = session["user_id"])
            # find the latest order number (for inserting in the orderbook)
            order_num = db.execute("SELECT order_num FROM portfolio where id = :id ORDER BY order_num DESC", id = session["user_id"])[0]['order_num']
            # insert the order in the orderbook
            db.execute("INSERT INTO orderbook VALUES (:order_num, :symbol, :amount, :price, CURRENT_TIMESTAMP, :ordertype)", order_num = order_num, symbol = symbol.upper(), amount = amount, price = quote['price'], ordertype = "SELL")
            # update the users cash balance in the database
            db.execute("UPDATE users set cash = :cash + :amount * :price WHERE id = :id", cash = cash, amount = int(amount),  price = quote['price'], id = session["user_id"])
            return redirect(url_for("index"))
    else:
        # else if user reached route via GET (as by clicking a link or via redirect)
        return render_template("sell.html")
