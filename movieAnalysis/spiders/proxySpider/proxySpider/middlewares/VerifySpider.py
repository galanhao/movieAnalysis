from scrapy import signals


class Middleware(object):

    def spider_closed(self, spider, reason):
        print("结束")