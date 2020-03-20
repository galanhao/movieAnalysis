# -*- coding: utf-8 -*-
import datetime
import random

import scrapy
from django.db.models import Q
from scrapy.http import HtmlResponse

from proxyManager.models import Proxy
from proxySpider.confs.testConf import HTTP_TEST_LIST, HTTPS_TEST_LIST, ANONYMITY_TEST_LIST, AREA_TEST_LIST

from proxySpider.items import ProxyItem
from proxySpider.utils.getAreas import getArea_ip138, getArea_default
from proxySpider.utils.getAnonymitys import getProtocol_default
from proxySpider.utils.responseTests import responseTest_default
from proxySpider.utils.verify import errorIgnored, verifyResponse, verifyItem


class VerifySpider(scrapy.Spider):
    name = 'verify'
    allowed_domains = ['*']

    def __init__(self, name=None, **kwargs):
        super().__init__(name=None, **kwargs)
        self.RETRY_HTTP_CODECS = 2
        self.DOWNLOAD_TIMEOUT = 26

    def start_requests(self):
        # proxys = Proxy.objects.values("ip", "port").filter(verify_time=None)
        # proxys = Proxy.objects.values("ip", "port").filter(source="genericSpiderjiangxianli").filter(http=1)
        # proxys = Proxy.objects.values("ip", "port").filter(source="genericSpiderjiangxianli").filter(http=0).filter(https=0)
        # proxys = Proxy.objects.values("ip", "port").filter(source="IPPOOL").filter(area="0")[:30]
        proxys = Proxy.objects.values("ip", "port").filter(Q(http=-1) | Q(https=-1))
        # proxys = Proxy.objects.values("ip", "port").all()[:60]
        # proxys = []
        for proxy in proxys:
            print(proxy)



            # TODO... 验证HTTP
            test_demo = random.choice(HTTP_TEST_LIST)
            yield scrapy.Request(url=test_demo["url"], meta={
                "proxy": "http://{}:{}".format(proxy["ip"], proxy["port"]),
                "ip": proxy["ip"],
                "port": proxy["port"],
                "flag": "HTTP",
                "reponseTest": test_demo["callbalk"],
                "dont_retry": False

            }, dont_filter=True,
            callback=self.verifyHTTP)



            # TODO... 验证HTTPS
            test_demo = random.choice(HTTPS_TEST_LIST)
            yield scrapy.Request(url=test_demo["url"], meta={
                "proxy": "https://{}:{}".format(proxy["ip"], proxy["port"]),
                "ip": proxy["ip"],
                "port": proxy["port"],
                "flag": "HTTPS",
                "getProtocol": test_demo["callbalk"],
                "dont_retry": False
            }, dont_filter=True, callback=self.verifyHTTPS)

    @verifyResponse
    def verifyHTTP(self, response):
        # print(response.body)
        responseTest = response.meta.get("responseTest", responseTest_default)
        ip = response.meta.get("ip", None)
        port = response.meta.get("port", None)
        print(ip, port)
        result, speed = responseTest(response)
        print(result, speed)
        item = ProxyItem()
        if result:
            item["flag"] = "verifyHTTP"
            item["ip"] = ip
            item["port"] = port
            item["http"] = 1
            item["speed"] = speed
        else:
            item["flag"] = "verifyHTTP"
            item["ip"] = ip
            item["port"] = port
            item["http"] = 0
        yield verifyItem(item)
        if result:
            request= self.startAnonymityTest(item)
            print(request)
            yield request

    @verifyResponse
    def verifyHTTPS(self, response):
        # print(response.body)
        responseTest = response.meta.get("responseTest", responseTest_default)
        ip = response.meta.get("ip", None)
        port = response.meta.get("port", None)
        print(ip, port)
        result, speed = responseTest(response)
        print(result, speed)
        item = ProxyItem()
        if result:
            item["flag"] = "verifyHTTPS"
            item["ip"] = ip
            item["port"] = port
            item["https"] = 1
            item["speed"] = speed
        else:
            item["flag"] = "verifyHTTPS"
            item["ip"] = ip
            item["port"] = port
            item["https"] = 0
        yield verifyItem(item)
        if result:
            request = self.startAnonymityTest(item)
            print(request)
            yield request

    def startAnonymityTest(self, item):
        test_demo = None
        protocol = None
        if item.get("http", -1) == 1:
            test_demo = random.choice(ANONYMITY_TEST_LIST["HTTP"])
            protocol = "http"
        elif item.get("https", -1) == 1:
            test_demo = random.choice(ANONYMITY_TEST_LIST["HTTPS"])
            protocol = "https"
        if test_demo == None or protocol == None:
            return None
        print("开始验证匿名性", "proxy->{}://{}:{}".format(protocol, item["ip"], item["port"]), test_demo["url"])
        return scrapy.Request(url=test_demo["url"], meta={
            "flag": "ANONYMITY",
            "ip": item["ip"],
            "port": item["port"],
            "proxy": "{}://{}:{}".format(protocol, item["ip"], item["port"]),
            "protocol": protocol,
            "dont_retry": False,
            "getAnonymity": test_demo["callbalk"],
        }, dont_filter=True, callback=self.getANONYMITY)

    def startAreaTest(self, item, protocol = None):
        test_demo = None

        ip = item["ip"]
        port = item["port"]
        test_demo = random.choice(AREA_TEST_LIST)
        print("test_demo, protocol")
        print(test_demo, protocol)
        print(test_demo == None , protocol == None)
        if test_demo == None and protocol == None:
            print("进入了")
            return None
        test_url = test_demo["url"]
        if test_demo["useIP"]:
            test_url = test_demo["url"].format(ip)
        return scrapy.Request(url=test_url,meta={
            "flag": "AREA",
            "ip": ip,
            "port": port,
            "proxy": "{}://{}:{}".format(protocol, ip, port),
            "getArea": test_demo["callbalk"],
            "dont_retry": False
        }, dont_filter=True, callback=self.getAREA)



    @verifyResponse
    def getANONYMITY(self, response):
        print("匿名性测试回执：")
        print(response.status)
        print(response.body)
        ip = response.meta["ip"]
        port = response.meta["port"]
        protocol = response.meta.get("protocol", "http")
        getAnonymity = response.meta.get("getAnonymity", getProtocol_default)
        result, anonymity, speed = getAnonymity(response)
        print(result, anonymity, speed)
        item = ProxyItem()
        if result:
            item["flag"] = "ANONYMITY"
            item["ip"] = ip
            item["port"] = port
            item["speed"] = speed
            item["anonymity"] = anonymity
        else:
            item["flag"] = "ANONYMITY"
            item["ip"] = ip
            item["port"] = port
            item["anonymity"] = 0
        yield verifyItem(item)
        if result:
            print("开始测试地域", protocol)
            request = self.startAreaTest(item, protocol)
            print(request)
            yield request


    @verifyResponse
    def getAREA(self, response):
        print("地域测试回执：")
        print(response)
        print(response.meta)
        ip = response.meta["ip"]
        port = response.meta["port"]
        getArea = response.meta.get("getArea", getArea_default)
        area = getArea(response)
        print("get area", area)
        areaItem = ProxyItem()
        areaItem["ip"] = ip
        areaItem["port"] = port
        areaItem["flag"] = "AREA"
        areaItem["area"] = area
        yield verifyItem(areaItem)





