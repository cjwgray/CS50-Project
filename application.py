import os.path
import pandas as pd
from cs50 import SQL
from flask import Flask, flash, redirect, render_template,session, request, url_for, make_response
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
application = Flask(__name__, template_folder="templates")



# Configure session to use filesystem (instead of signed cookies)
application.config["SESSION_PERMANENT"] = False
application.config["SESSION_TYPE"] = "filesystem"
Session(application)

# SQLite database db

db = SQL("sqlite:///ClarenceGamingDen.db")



@application.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

if not os.path.exists("polls.csv"):
    structure = {
        "pid": [],
        "poll": [],
        "option1": [],
        "option2": [],
        "option3": [],
        "votes1": [],
        "votes2": [],
        "votes3": []
    }

    pd.DataFrame(structure).set_index("pid").to_csv("polls.csv")

polls_df = pd.read_csv("polls.csv").set_index("pid")







@application.route("/login", methods=["GET", "POST"])
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
        session["username"] = rows[0]["username"]
        return redirect("/")
    
    else:
        return render_template("login.html")
    
    




@application.route("/logout")
def logout():
    session.clear()
    
    return redirect("/")



@application.route("/register", methods=["GET", "POST"])
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
    





@application.route("/")
@login_required
def index():
    """Home page"""
    """user_id = session.get("user_id")"""
    username = session.get("username")
        
    return render_template("index.html", polls=polls_df, username=username)

@application.route('/user')
@login_required
def user():
    
    username = session.get("username")
    
    return render_template("user.html", username=username)
 
       
       
       
       

@application.route("/polls/<pid>")
@login_required
def polls(pid):
    poll = polls_df.loc[int(pid)]
    return render_template("show_poll.html", poll=poll)

@application.route("/polls", methods=["GET", "POST"])
@login_required
def create_poll():
    if request.method == "GET":
        return render_template("new_poll.html")
    elif request.method == "POST":
        poll = request.form['poll']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']
        polls_df.loc[max(polls_df.index.values) + 1] = [poll, option1, option2, option3, 0, 0, 0]
        polls_df.to_csv("polls.csv")
        return redirect(url_for("index"))
    
    
@application.route("/vote/<pid>/<option>")
@login_required
def vote(pid, option):
    username = session.get("username")
    if request.cookies.get(f"vote_{pid}_cookie") is None:
        polls_df.at[int(pid), "votes"+str(option)]+= 1
        polls_df.to_csv("polls.cvs")
        response = make_response(redirect(url_for("polls", pid=pid)))
        response.set_cookie(f"vote_{pid}_cookie", str(option))
        return response
    else:
        return render_template("nomorevotes.html", username=username) 
    
    

@application.route("/baldursgate3")
@login_required
def baldursgate3():
    """The baldurs gate 3 game page"""
    username = session.get("username")
    return render_template("baldursgate3.html", username=username)


@application.route("/cyberpunk2077PL")
@login_required
def cyberpunk2077PL():
    """The cyberpunk2077PL game page"""
    username = session.get("username")
    return render_template("cyberpunk2077PL.html", username=username)

@application.route("/alanwake2")
@login_required
def alanwake2():
    """The Alan Wake 2 game page"""
    username = session.get("username")
    return render_template("alanwake2.html", username=username)

@application.route("/favorite")
@login_required
def favorite():
    """This page is for the quiz"""
    username = session.get("username")
    return render_template("favorite.html", username=username)




@application.route("/comment", methods =["GET", "POST"])
@login_required
def comment():
    """This is for the users to leave comments"""
    username = session.get("username")
    if request.method == "GET":
       
        comments = db.execute("SELECT send as comment, username, date, id FROM comments ORDER BY date DESC")
        
        return render_template("comment.html", comments=comments, username=username)
    else:
        comment = request.form.get("comment")
        

        if not comment:
            return apology("No Empty Fields")

        db.execute("INSERT INTO comments (username, send) VALUES (?,?)", username, comment)
        comments = db.execute("SELECT send as comment, username, date, id FROM comments ORDER BY date DESC")
       

        #username = session.get("username")
       
        return render_template("comment.html", comments=comments)
    
    
if __name__ == "__main__":
    application.run(host="localhost", debug=True)