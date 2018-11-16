import os
from flask import Flask, render_template, session, redirect, request

app = Flask(__name__)

app.secret_key = "random12345"

online_users = []

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Index route and view. If the form is POSTed then
    create a session variable called username. This
    variable will persist until the browser is restarted.
    The online_users global list stores everyone who is
    currently logged in.
    """
    if request.method == "POST":
        session["username"] = request.form["username"]
        online_users.append(request.form["username"])
        return redirect("/user")
    
    if "username" in session:
        if session["username"] not in online_users:
            online_users.append(session["username"])
        
        return redirect("/user")
    
    return render_template("index.html")
    
@app.route("/user")
def user():
    """
    Returns the user template and sends through the username
    and online_users list
    """
    return render_template("user.html", users=online_users, username=session["username"])

@app.route("/logout")
def logout():
    """
    Gets the index of where the current username is in the list
    and pops (or removes) it. Then clears the session, so that
    the username is deleted from the browser.
    """
    username = session["username"]
    session.clear()
    online_users.pop(online_users.index(username))
    return redirect("/")
    
if __name__ == "__main__":
    app.run(os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", "8080")),
            debug=True)
