# 一个非常简单的框架，为简单的python代码构建前端页面，依托flask


## 1. 无权限验证的版本

`func.py` 中是你的python代码或处理逻辑

`app.py` 为 flask 的启动入口

`start.bat` 为 windows 的启动脚本，会同时启动前端和后端

`index.html` 为 服务展示网页

---

`ENABLE_AUTH = True` 可以选择是否启用网站密码校验


`auth.py` 为 flask(带校验) 的启动入口

`login.html` 为 校验登录网站





