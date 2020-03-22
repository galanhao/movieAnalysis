# -*- coding: utf-8 -*-

import scrapy


# from proxySpider.conf import VERIFY_LIST, get_random_base_headers
from proxySpider.items import ProxyItem

from proxySpider.confs.genericSpiderConf import SPIDER_NAME_LIST as SNL
from proxySpider.confs.genericSpiderConf import SPIDER_INFO_LIST as SIL



class GenericSpider(scrapy.Spider):
    name = 'genericSpider'


    allowed_domains = ['*']
    start_urls = []
    def __init__(self, **kwargs):
        # print(kwargs)
        child_name = kwargs.get("cn", "")
        if child_name in SNL:
            # print(SIL)


            if SIL[SNL.index(child_name)].get("useRange", False):
                self.logger.info("使用了useRange")
                url_format = SIL[SNL.index(child_name)]["url"]
                self.logger.info("url_format:{}".format(url_format))
                start_index = int(kwargs.get("si", "1"))
                end_index = int(kwargs.get("ei", "1"))
                self.logger.info("start_index: {}, end_index: {}".format(start_index, end_index))
                self.start_urls = [url_format.format(x) for x in range(start_index, end_index)]
            else:
                self.logger.info("没有使用useRange")
                self.start_urls = SIL[SNL.index(child_name)]["url"]
            self.INFO = SIL[SNL.index(child_name)]
            super().__init__(name=self.name+""+child_name, **kwargs)
            # print(self.start_urls)
            self.logger.info(self.start_urls)
            self.download_delay = 3
        else:
            # print("没有爬虫： ", child_name)
            self.logger.info("没有爬虫： ", child_name)
    def start_requests(self):
        for url in self.start_urls:
            self.logger.info("开始请求，{}".format(url))
            yield scrapy.Request(url, dont_filter=True)
    def parse(self, response):
        self.logger.info("来至{}的响应，code: {}".format(response.url, response.status))
        # print(response.body)
        oneLines = []
        for oneLine in self.INFO["oneLine"]:
            self.logger.info("处理 oneLine:{}".format(oneLine))
            oneLines.extend(response.xpath(oneLine))
        for oneLine in oneLines:
            self.logger.info("拿到oneline响应: {}".format(oneLine))
            ip = oneLine.xpath(self.INFO["ip"]).extract_first(None)
            port = oneLine.xpath(self.INFO["port"]).extract_first(None)
            if ip!=None and port!=None:
                self.logger.info("拿到的 ip:{}, port:{}".format(ip, port))
                ip = ip.strip()
                port = port.strip()
                # print(ip, port)
                if ip.count(".") == 3:
                    self.logger.info("{}:{}#可以进入管道".format(ip, port))
                    item = ProxyItem()
                    item["ip"] = ip
                    item["port"] = port
                    item["source"] = self.name
                    item["flag"] = "crawl"
                    yield item
                else:
                    self.logger.info("这玩意不是ip啊{}".format(ip))

