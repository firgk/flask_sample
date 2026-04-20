from flask import *
from threading import*
from flask_httpauth import HTTPBasicAuth

from func import *


app = Flask(__name__,static_folder="", template_folder="")
auth = HTTPBasicAuth()



users = {
    "admin": "123456"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username
    return None



@app.before_request
def global_auth_check():
    """
    全局自动鉴权（所有路由自动需要登录，不用写装饰器）
    包含 Cookie 持久化登录
    """
    # 放行静态资源（可选）
    if request.path.startswith("/static"):
        return

    # 1. 检查是否有持久化 Cookie → 已登录直接放行
    if request.cookies.get("logged_in") == "yes":
        return

    # 2. 没有登录 → 强制触发 flask-httpauth 登录
    auth_response = auth.login_required(lambda: None)()
    return auth_response


def set_login_cookie(response):
    """设置7天持久化登录 Cookie"""
    response.set_cookie("logged_in", "yes", max_age=7 * 24 * 3600)
    return response


# ================ 路由 ================

@app.route('/')
@auth.login_required
def index():
    content='XXX'
    resp = make_response(render_template('index.html', content=content))
    return set_login_cookie(resp)  # 登录成功自动持久化

    
# printhello_flask → 展示：后台异步执行函数，不返回结果给页面
@app.route('/printhello_flask')
def printhello_flask():
    thread = Thread(target=printhello)
    thread.start()
    return render_template('index.html')


# returnhello_flask → 展示：执行函数并把结果返回给网页显示
@app.route('/returnhello_flask')
def returnhello_flask():
    content=returnhello()
    return render_template('index.html',content=content)
    



# if you need some args
# @app.route('/re_make_picer/<id>')
# def re_make_picer(id):
#     thread = Thread(target=re_make_pic, args=(id,))
#     thread.start()
#     return redirect(url_for('index'))






if __name__ == '__main__':
    app.run(debug=True)
