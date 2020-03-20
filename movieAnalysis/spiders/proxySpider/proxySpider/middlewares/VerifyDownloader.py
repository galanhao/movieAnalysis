from scrapy.core.downloader.handlers.http11 import TunnelError
from scrapy.http import HtmlResponse
from twisted.internet.error import  TCPTimedOutError, ConnectionRefusedError, TimeoutError
from twisted.web._newclient import ResponseNeverReceived

from proxyManager.models import Proxy
from proxySpider.confs.paramConf import BAD_RESPONSE_TAG

from proxySpider.spiders.verify import VerifySpider


class Middleware(object):
    EXCEPTIONS_TO_IGNORED = (TCPTimedOutError,  ConnectionRefusedError,
                             TunnelError, TimeoutError, ResponseNeverReceived)

    def process_request(self, request, spider):
        # print("spider.name ",spider.name)
        # print(request.meta, request.url)
        # print(request.headers)
        return None


    def process_response(self, request, response, spider):
        if isinstance(spider, VerifySpider):
            # print(request.meta["ip"], request.meta["port"])
            # print(request.url)
            # print("返回码 ", response.status)
            if response.status !=200:
                if request.meta["flag"].lower()=="area":
                    Proxy.objects.filter(ip=request.meta["ip"], port=request.meta["port"]) \
                        .update(**{request.meta["flag"].lower(): None})
                else:
                    Proxy.objects.filter(ip=request.meta["ip"], port=request.meta["port"]) \
                        .update(**{request.meta["flag"].lower(): 0})
        # print(request, response)
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(spider, VerifySpider) \
                and  isinstance(exception, self.EXCEPTIONS_TO_IGNORED):
            # print(request.meta["ip"], request.meta["port"])
            # print("错误信息 ",exception)
            if request.meta["flag"].lower() == "area":
                Proxy.objects.filter(ip=request.meta["ip"], port=request.meta["port"]).update(**{request.meta["flag"].lower(): None})
            else:
                Proxy.objects.filter(ip=request.meta["ip"], port=request.meta["port"]).update(
                    **{request.meta["flag"].lower(): 0})
            response = HtmlResponse(url=BAD_RESPONSE_TAG)
            return response
