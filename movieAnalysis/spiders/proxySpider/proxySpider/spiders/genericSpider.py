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
            start_index = int(kwargs.get("si", "1"))
            end_index = int(kwargs.get("ei", "5"))
            url_format = SIL[SNL.index(child_name)]["url"]
            self.start_urls = [url_format.format(x) for x in range(start_index, end_index)]
            self.INFO = SIL[SNL.index(child_name)]
            super().__init__(name=self.name+""+child_name, **kwargs)
            # print(self.start_urls)
            self.logger.info(self.start_urls)
            self.download_delay = 3
        else:
            # print("没有爬虫： ", child_name)
            self.logger.info("没有爬虫： ", child_name)

    def parse(self, response):
        # print(response)
        # print(response.body)
        oneLines = []
        for oneLine in self.INFO["oneLine"]:
            # print(oneLine)
            oneLines.extend(response.xpath(oneLine))
        for oneLine in oneLines:
            # print(oneLine)
            ip = oneLine.xpath(self.INFO["ip"]).extract_first(None)
            port = oneLine.xpath(self.INFO["port"]).extract_first(None)
            if ip and port:
                # print(type(ip))
                # print(type(port))
                ip = ip.strip()
                port = port.strip()
                # print(ip, port)
                item = ProxyItem()
                item["ip"] = ip
                item["port"] = port
                item["source"] = self.name
                item["flag"] = "crawl"
                yield item

