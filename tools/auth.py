from flask import make_response, redirect, url_for, render_template, request

# 只需要一个固定密码
LOGIN_PASSWORD = "123456"

IP_LIMIT_ENABLED = True

if IP_LIMIT_ENABLED:
    from tools.ip_limit import * 


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

        #  --- 耦合 ip_limit start
        ip = request.remote_addr
        if IP_LIMIT_ENABLED:
            msg = check_ip_limit(ip)
            if msg:
                return render_template("login.html", error=msg)
   
        if request.method == "POST":
            add_login_count(ip)
        #  --- 耦合 ip_limit done


        if request.cookies.get("logged_in") == "yes":
            return redirect(url_for("index"))
        
        if request.method == "GET":
            return render_template("login.html")
        
        # 只获取密码，不验证用户名
        password = request.form.get("password", "").strip()
        
        if password == LOGIN_PASSWORD:
            resp = make_response(redirect(url_for("index")))
            resp.set_cookie("logged_in", "yes", max_age=7*24*3600)
            return resp

        
        return render_template("login.html", error="密码错误")

    # 退出路由
    @app.route('/logout')
    def logout():
        resp = make_response(redirect(url_for("login")))
        resp.set_cookie("logged_in", "", expires=0)
        return resp
