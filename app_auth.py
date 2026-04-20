from flask import Flask, render_template, request, make_response, redirect, url_for
from threading import Thread

# 导入你的外部函数
from func import *

# ================ 初始化应用 ================
app = Flask(__name__, static_folder="", template_folder="")

# 登录用户配置（手写账号密码）
USER_DATA = {
    "admin": "123456"
}

# ================ 手写全局登录校验（核心） ================
@app.before_request
def check_login():
    """
    所有请求前自动校验登录状态
    1. 放行登录页、退出接口
    2. 已登录 → 放行
    3. 未登录 → 跳转到登录页
    """
    # 不需要登录就能访问的路径
    free_paths = ["/login", "/logout"]
    
    # 如果是放行路径，直接跳过
    if request.path in free_paths:
        return
    
    # 检查 Cookie 是否登录
    if request.cookies.get("logged_in") != "yes":
        # 未登录 → 重定向到登录页
        return redirect(url_for("login"))

# ================ 手写登录/退出路由 ================
@app.route("/login", methods=["GET", "POST"])
def login():
    """登录页面 + 登录校验"""
    # 如果已经登录，直接去首页
    if request.cookies.get("logged_in") == "yes":
        return redirect(url_for("index"))

    # GET 请求 → 返回登录表单
    if request.method == "GET":
        return render_template("login.html")

    # POST 请求 → 校验账号密码
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    # 账号密码正确
    if username in USER_DATA and USER_DATA[username] == password:
        resp = make_response(redirect(url_for("index")))
        # 设置7天持久化登录 Cookie
        resp.set_cookie("logged_in", "yes", max_age=7*24*3600)
        return resp

    # 账号密码错误 → 返回登录页并提示
    return render_template("login.html", error="账号或密码错误")

@app.route('/logout')
def logout():
    """退出登录（清除 Cookie）"""
    resp = make_response(redirect(url_for("login")))
    resp.set_cookie("logged_in", "", expires=0)
    return resp











# ================ 业务路由 ================
@app.route('/')
def index():
    content = '空'
    return render_template('index.html', content=content)

@app.route('/printhello_flask')
def printhello_flask():
    # 后台异步执行
    Thread(target=printhello).start()
    return redirect(url_for('index'))

@app.route('/returnhello_flask')
def returnhello_flask():
    content = returnhello()
    return render_template('index.html', content=content)


















# ================ 启动 ================
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")