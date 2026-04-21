from flask import make_response, redirect, url_for, render_template, request

# 账号配置
USER_DATA = {
    "admin": "123456"
}

# 初始化认证：把 app 传进来绑定
def init_auth(app):
    # 全局登录校验
    @app.before_request
    def check_login():
        free_paths = ["/login", "/logout"]
        if request.path in free_paths:
            return
        if request.cookies.get("logged_in") != "yes":
            return redirect(url_for("login"))

    # 登录路由
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.cookies.get("logged_in") == "yes":
            return redirect(url_for("index"))
        
        if request.method == "GET":
            return render_template("login.html")
        
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        
        if username in USER_DATA and USER_DATA[username] == password:
            resp = make_response(redirect(url_for("index")))
            resp.set_cookie("logged_in", "yes", max_age=7*24*3600)
            return resp
        
        return render_template("login.html", error="账号或密码错误")

    # 退出路由
    @app.route('/logout')
    def logout():
        resp = make_response(redirect(url_for("login")))
        resp.set_cookie("logged_in", "", expires=0)
        return resp





