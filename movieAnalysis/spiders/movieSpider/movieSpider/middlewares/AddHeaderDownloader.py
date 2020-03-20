import random

from scrapy.http import Headers

from spiders.movieSpider.movieSpider.conf import USER_AGENTS, BASE_HEADERS



class Middleware(object):
    encoding = "utf-8"
    def process_request(self, request, spider):
        ADD_HEADER_LIST = [
            {
                "url": "http://m.maoyan.com/mmdb/comments/movie/",
                "headers": {
                    'User-Agent': random.choice(USER_AGENTS)
                }
            },
            {
                "url": "https://maoyan.com/board/",
                "headers" : BASE_HEADERS
            },
            {
                "url": "https://maoyan.com/films/",
                "headers": BASE_HEADERS,
                "additional": {
                    "Referer": "https://maoyan.com/board/4"
                }
            }

        ]
        for header in ADD_HEADER_LIST:
            print("add Header", request.url,header["url"])
            if request.url.startswith(header["url"]):
                tmp = header["headers"]
                if "additional" in tmp:
                    tmp.update(header["additional"])

                request.headers = Headers(tmp, encoding=self.encoding)
                print(request.url, tmp)
                break


    def process_response(self, request, response, spider):
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        # print("AddHeaderMiddleware", response)
        return response