from time import strftime

# 配置
# 每天最多登录的尝试次数（不管失败还是正确,有cookies,谁家好人退了又登录）
MAX_LOGIN_PER_DAY = 100
ip_login_count = {}

# 检查IP是否超限
def check_ip_limit(ip):
    today = strftime("%Y-%m-%d")
    key = f"{ip}_{today}"
    
    if ip_login_count.get(key, 0) >= MAX_LOGIN_PER_DAY:
        return "今日登录次数已达上限，请明天再试"
    return None

# 计数 +1
def add_login_count(ip):
    today = strftime("%Y-%m-%d")
    key = f"{ip}_{today}"
    ip_login_count[key] = ip_login_count.get(key, 0) + 1