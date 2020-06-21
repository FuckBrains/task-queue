from flask import render_template, request
from .. import app


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    
    
@app.route("/send-email", methods=["GET", "POST"])
def send_email():
    if request.method == "GET":
        return render_template("send_email.html")
