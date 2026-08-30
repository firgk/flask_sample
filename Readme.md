# 一个非常简单的框架，为简单的 Python 代码构建前端页面，依托 Flask

## 文件介绍

`func.py` 中是你的 Python 代码或处理逻辑。

`app.py` 为 Flask 的启动入口。

`start.bat` 为 Windows 的启动脚本，会同时启动前端和后端。

`index.html` 为服务展示网页。

---

`ENABLE_AUTH` 可以选择是否启用网站密码校验。

`tools/auth.py` 为登录鉴权逻辑，登录状态使用 Flask 签名 Session，不能再通过伪造 `logged_in=yes` Cookie 绕过。

`login.html` 为登录页面。

启动前必须设置登录密码，密码不再写入仓库：

```bash
export LOGIN_PASSWORD='你的密码'
python app.py
```

Windows CMD：

```bat
set LOGIN_PASSWORD=你的密码
python app.py
```

可选设置固定 Session 签名密钥；不设置时每次启动会随机生成，因此重启后需要重新登录：

```bash
export FLASK_SECRET_KEY='足够长的随机字符串'
```

---

`IP_LIMIT_ENABLED` 可以选择是否启用 IP 校验，辅助防爆破。

`tools/ip_limit.py` 为 IP 登录次数限制。
