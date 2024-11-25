# config.py
import random

def generate_bid():
    """生成随机的bid值"""
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(characters) for _ in range(11))

# 基础配置
MOVIE_ID = '35183325'  # 女人世界的豆瓣ID
MAX_PAGES = 50         # 最大爬取页数
REQUEST_TIMEOUT = 30   # 请求超时时间
RETRY_TIMES = 3        # 请求重试次数
RETRY_DELAY = 5        # 重试延迟时间
DELAY_MIN = 2          # 最小延迟时间
DELAY_MAX = 5          # 最大延迟时间

# Cookie配置
COOKIES = {
    'bid': 'jtyT9nZw4gg',
    '__eoi': 'ID=14c04b91bc68ceca:T=1732072420:RT=1732072420:S=AA-AfjaBswaTZfPLJ7dQccclun19',
    'dbcl2': '"262904750:ScwXC96lZhY"',
    'push_noty_num': '0',
    'push_doumail_num': '0',
    'ck': 'l5ZU',
    'll': '"108288"',
    'ap_v': '0,6.0',
    'frodotk_db': '"095f24d2b201e7651c1d6e781605b62f"'
}

# 请求头配置
HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Referer': f'https://movie.douban.com/subject/{MOVIE_ID}/comments?limit=20&status=P&sort=new_score',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
}

# 构建Cookie字符串
COOKIE_STRING = '; '.join([f'{k}={v}' for k, v in COOKIES.items()])
HEADERS['Cookie'] = COOKIE_STRING