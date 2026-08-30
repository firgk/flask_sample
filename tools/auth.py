import os

from flask import redirect, render_template, request, session, url_for

# 登录密码必须通过环境变量提供，避免把密码提交到公开仓库
LOGIN_PASSWORD = os.environ.get("LOGIN_PASSWORD")

IP_LIMIT_ENABLED = True

if IP_LIMIT_ENABLED:
    from tools.ip_limit import *


# 初始化认证：把 app 传进来绑定
def init_auth(app):
    if not LOGIN_PASSWORD:
        raise RuntimeError("LOGIN_PASSWORD environment variable is required")

    @app.before_request
    def check_login():
        free_paths = ["/login", "/logout"]
        if request.path in free_paths:
            return
        if not session.get("logged_in"):
            return redirect(url_for("login"))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        ip = request.remote_addr
        if IP_LIMIT_ENABLED:
            msg = check_ip_limit(ip)
            if msg:
                return render_template("login.html", error=msg)

        if request.method == "POST":
            add_login_count(ip)

        if session.get("logged_in"):
            return redirect(url_for("index"))

        if request.method == "GET":
            return render_template("login.html")

        password = request.form.get("password", "").strip()

        if password == LOGIN_PASSWORD:
            session.permanent = True
            session["logged_in"] = True
            return redirect(url_for("index"))

        return render_template("login.html", error="密码错误")

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login"))
