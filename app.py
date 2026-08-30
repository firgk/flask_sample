# app.py

import os
import secrets
from datetime import timedelta
from threading import Thread

from flask import Flask, render_template

from func import printhello, returnhello

app = Flask(__name__, static_folder="", template_folder="")
app.config.update(
    SECRET_KEY=os.environ.get("FLASK_SECRET_KEY") or secrets.token_hex(32),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=timedelta(days=7),
)

# ================ 引入认证================

ENABLE_AUTH = True

if ENABLE_AUTH:
    from tools.auth import init_auth

    init_auth(app)


@app.route("/")
def index():
    content = "空"
    return render_template("index.html", content=content)


@app.route("/printhello_flask")
def printhello_flask():
    thread = Thread(target=printhello)
    thread.start()
    return render_template("index.html")


@app.route("/returnhello_flask")
def returnhello_flask():
    content = returnhello()
    return render_template("index.html", content=content)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
