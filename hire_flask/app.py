from flask import Flask, render_template, request, redirect, url_for
import logic

app = Flask(__name__)

@app.route("/")
def home():
    profiles = logic.load_profiles()
    return render_template("index.html", profiles=profiles)

@app.route("/add", methods=["GET", "POST"])
def add_profile():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        address = request.form["address"]
        contact = request.form["contact"]
        occupation = request.form["occupation"]
        logic.add_profile(name, age, address, contact, occupation)
        return redirect(url_for("home"))
    return render_template("add_profile.html")

@app.route("/rate/<name>", methods=["POST"])
def rate(name):
    rating = int(request.form["rating"])
    logic.rate_profile(name, rating)
    return redirect(url_for("home"))

@app.route("/leaderboard")
def leaderboard():
    leaders = logic.get_leaderboard()
    return render_template("leaderboard.html", profiles=leaders)

@app.route("/chat/<name>", methods=["GET", "POST"])
def chat(name):
    if request.method == "POST":
        sender = request.form["sender"]
        message = request.form["message"]
        logic.send_message(sender, name, message)
        return redirect(url_for("chat", name=name))
    messages = logic.get_chat("You", name)  
    return render_template("chat.html", name=name, messages=messages)

if __name__ == "__main__":
    app.run(debug=True)
