# from requests.http import Response
from scrapy.core.downloader.handlers.http11 import TunnelError
from scrapy.http import HtmlResponse
from twisted.internet.error import TCPTimedOutError, ConnectionRefusedError, TimeoutError

from proxyManager.models import Proxy



class Middleware(object):
    EXCEPTIONS_TO_IGNORED = (TCPTimedOutError,  ConnectionRefusedError,
                             TCPTimedOutError, TunnelError, TimeoutError,)

    def process_request(self, request, spider):
        # print("spider.name ",spider.name)
        # print(request.meta, request.url)
        # print(request.headers)
        return None


    def process_response(self, request, response, spider):
        # print(request, response)
        return response

    def process_exception(self, request, exception, spider):
        pass
        # if isinstance(exception, self.EXCEPTIONS_TO_IGNORED):
        #     print("cuowu ",exception)
        #     # Proxy.objects.filter(ip=request.meta["ip"]).delete()
        #     print("SC")
        #     response = HtmlResponse(url=BAD_RESPONSE_TAG)
        #     # response.request=request
        #     return response
        # else:
        #     print("cuowu1 ", exception)
        #     Proxy.objects.filter(ip=request.meta["ip"]).delete()
        #     print("SC1")
        #     response = HtmlResponse(url=BAD_RESPONSE_TAG)
        #     # response.request=request
        #     return response
