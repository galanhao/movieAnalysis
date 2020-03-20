import random

from DB.mongdbCli import MongoDBCli
from proxySpider.confs.paramConf import BASE_HEADERS, USER_AGENTS

DEFAULT_HEADER = BASE_HEADERS

SPIDER_INFO_LIST = [
    {
        "name": "xici",
        "url": "https://www.xicidaili.com/nn/{}",
        "header": {
            "Host": "www.xicidaili.com",
            "Upgrade-Insecure-Requests": "1",
            'Connection': 'keep-alive',
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9"
        },
        "oneLine": ["//tr", ],
        "ip": "td[2]/text()",
        "port": "td[3]/text()"
    },
    {
        "name": "kuaidaili",
        "url": "https://www.kuaidaili.com/free/inha/{}/",
        "header": {
            "Host": "www.kuaidaili.com",
            "Upgrade-Insecure-Requests": "1",
            'Connection': 'keep-alive',
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9"
        },
        "oneLine": ["//tr", ],
        "ip": "td[1]/text()",
        "port": "td[2]/text()"
    },
    {
        "name": "7yip",
        "url": "https://www.7yip.cn/free/?action=china&page={}",
        "header": {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "cookie": "__guid=16617264.951008932595936500.1581574311010.6846; Hm_lvt_96901db7af1741c2fd2d52f310d78eaa=1584509723; monitor_count=4; Hm_lpvt_96901db7af1741c2fd2d52f310d78eaa=1584509752",
            "pragma": "no-cache",
            "referer": "https://www.7yip.cn/free/?action=china&page=1",
            "upgrade-insecure-requests": "1",
            "user-agent": random.choice(USER_AGENTS),
        },
        "oneLine": ["//tbody/tr", ],
        "ip": "td[1]/text()",
        "port": "td[2]/text()"
    },
    {
        "name": "jiangxianli",
        "url": "https://ip.jiangxianli.com/?page={}",
        "header": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Host": "ip.jiangxianli.com",
            "Pragma": "no-cache",
            "Referer": "https://ip.jiangxianli.com/?page=1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": random.choice(USER_AGENTS),
        },
        "oneLine": ["//tbody/tr", ],
        "ip": "td[1]/text()",
        "port": "td[2]/text()"
    },

]
db = MongoDBCli()
SPIDER_INFO_LIST = []
SPIDER_INFO_LIST .extend(db.getProxySpiderConfig())


SPIDER_NAME_LIST = [
    x["name"] for x in SPIDER_INFO_LIST
]
