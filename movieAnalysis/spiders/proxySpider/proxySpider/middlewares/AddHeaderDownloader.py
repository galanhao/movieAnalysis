import random

from scrapy.http import Headers

from proxySpider.confs.paramConf import USER_AGENTS
from proxySpider.confs.testConf import HTTP_TEST_LIST, HTTPS_TEST_LIST, AREA_TEST_LIST
from proxySpider.spiders.genericSpider import GenericSpider
from proxySpider.confs.genericSpiderConf import SPIDER_NAME_LIST as SNL, DEFAULT_HEADER

from proxySpider.confs.genericSpiderConf import SPIDER_INFO_LIST as SIL


class Middleware(object):
    encoding = "utf-8"

    def process_request(self, request, spider):
        ADD_HEADER_LIST = [
            {
                "url": "https://2020.ip138.com/",
                "header": {
                    "Accept": " text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                    "Accept-Encoding": " gzip, deflate, br",
                    "Accept-Language": " zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Cache-Control": " max-age=0",
                    "Connection": " keep-alive",
                    # "Cookie": " pgv_pvi=9052034048; ASPSESSIONIDQABRSRSA=KGKJDHEAHAEBDKOPFODCJAPG",
                    "Host": " 2020.ip138.com",
                    "Upgrade-Insecure-Requests": " 1",
                    "User-Agent": " Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",

                }
            },
            {
                "url": "http://httpbin.org/get",
                "header": {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "Cookie": "__guid=147723374.486925770027708200.1581480768812.5906; monitor_count=1",
                    "Host": "httpbin.org",
                    "Pragma": "no-cache",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
                }
            },
            {
                "url": "https://httpbin.org/get",
                "header": {
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "zh-CN,zh;q=0.9",
                    "cache-control": "no-cache",
                    "pragma": "no-cache",
                    "upgrade-insecure-requests": "1",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
                }
            },
        ]
        # 添加HTTP测试头信息
        ADD_HEADER_LIST.extend([{
            "url": x["url"],
            "header": x["header"],
        } for x in HTTP_TEST_LIST])
        ADD_HEADER_LIST.extend([{
            "url": x["url"],
            "header": x["header"],
        } for x in HTTPS_TEST_LIST])
        ADD_HEADER_LIST.extend([{
            "url": x["url"],
            "header": x["header"],
        } for x in AREA_TEST_LIST])
        if spider.name.startswith(GenericSpider.name) and spider.cn in SNL:
            header = SIL[SNL.index(spider.cn)].get("header", DEFAULT_HEADER)
            # print("add header", header)
            request.headers = Headers(header, encoding=self.encoding)
        else:
            # print("S", request.url)
            for add_header in ADD_HEADER_LIST:
                if request.url.startswith(add_header["url"]):
                    # print("add header", add_header["header"])
                    add_header["header"]["User-Agent"] = random.choice(USER_AGENTS)
                    request.headers = Headers(add_header["header"], encoding=self.encoding)
                    break
        return None

    def process_response(self, request, response, spider):

        return response

    def process_exception(self, request, exception, spider):
        pass
