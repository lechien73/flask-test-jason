import os
from flask import Flask, render_template, session, redirect, request

app = Flask(__name__)

app.secret_key = "random12345"

online_users = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session["username"] = request.form["username"]
        online_users.append(request.form["username"])
        return redirect("/user")
    
    if "username" in session:
        if session["username"] not in online_users:
            online_users.append(request.form["username"])
        
        return redirect("/user")
    
    return render_template("index.html")
    
@app.route("/user")
def user():
    return render_template("user.html", users=online_users, username=session["username"])

@app.route("/logout")
def logout():
    online_users.pop(online_users.index(session["username"]))
    session.clear()
    return redirect("/")
    
if __name__ == "__main__":
    app.run(os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", "8080")),
            debug=True)
