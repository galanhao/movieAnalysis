import datetime
import json
import random

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import TCPTimedOutError, DNSLookupError

from proxyManager.models import Proxy

import scrapy

from proxySpider.confs.paramConf import BAD_RESPONSE_TAG
from proxySpider.confs.testConf import ANONYMITY_TEST_LIST
from proxySpider.items import ProxyItem


def verifyResponse(func):
   def wrapper(*args, **kwargs):
       if args[1] and args[1].url != BAD_RESPONSE_TAG:
           return func(*args, **kwargs)
       return None
   return wrapper


def verifyItem(item):

    if isinstance(item, ProxyItem):
        proxy = Proxy.objects.filter(ip=item["ip"], port=item["port"]).first()
        protocol = 0
        if proxy.http == 1:
            protocol += 1
        if proxy.https == 1:
            protocol += 2
        item["protocol"] = protocol
        item["verify_time"] = datetime.datetime.now()
    return item







    # yield scrapy.Request(url=)





def errorIgnored(failure):
    print(failure)
    if failure.check(HttpError):
        # HttpError由HttpErrorMiddleware中间件抛出
        # 可以接收到非200 状态码的Response
        response = failure.value.response
        print('HttpError on %s', response.url)

    elif failure.check(DNSLookupError):
        # 此异常由请求Request抛出
        request = failure.request
        print('DNSLookupError on %s', request.url)

    elif failure.check(TimeoutError, TCPTimedOutError):
        request = failure.request
        print('TimeoutError on %s', request.url)
