import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///Project.db")



@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response




@app.route("/")
@login_required
def index():
    """Home page"""
    
    return render_template("index.html")


@app.route("/forspoken")
@login_required
def forspoken():
    """The Forspoke game page"""
    return render_template("forspoken.html")


@app.route("/hogwart")
@login_required
def hogwart():
    """The Hogwart game page"""
    return render_template("hogwart.html")

@app.route("/sw")
@login_required
def sw():
    """The Starwars: Surviver game page"""
    return render_template("sw.html")

@app.route("/favorite")
@login_required
def favorite():
    """This page is for the quiz"""
    return render_template("favorite.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)


        elif not request.form.get("password"):
            return apology("must provide password", 403)


        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))


        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")
    

@app.route('/username/<name>')
def username(name):
    return render_template("user.html", user_name=name)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if (request.method == "POST"):
        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')

        if not username:
            return apology('Please enter username.')
        elif not password:
            return apology('Please enter password.')
        elif not confirmation:
            return apology('Please confirm password.')
        if password != confirmation:
            return apology('Passwords do not match')

        hash = generate_password_hash(password)

        try:
            db.execute("INSERT INTO users(username, hash) VALUES (?, ?)", username, hash)
            return redirect('/')
        except:
            return apology('Username is already used.')
    else:
        return render_template("register.html")


@app.route("/comment", methods =["GET", "POST"])
@login_required
def comment():
    """This is for the users to leave comments"""
    if request.method == "GET":
        
        comments = db.execute("SELECT send as comment, date, id FROM comments ORDER BY date DESC")
        return render_template("comment.html", comments=comments)
    else:
        comment = request.form.get("comment")


        if not comment:
            return apology("No Empty Fields")

        db.execute("INSERT INTO comments (send) VALUES (?)", comment)
        comments = db.execute("SELECT send as comment, date, id FROM comments ORDER BY date DESC")


        return render_template("comment.html", comments=comments)







