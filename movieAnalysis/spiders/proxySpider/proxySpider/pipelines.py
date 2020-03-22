# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from proxyManager.models import Proxy


class ProxyPipeline(object):
    def process_item(self, item, spider):
        spider.logger.info("进入pipeline {}".format(item))
        flag = item.get("flag", False)
        if flag == "crawl":
            try:
                item.save()
            except BaseException as e:
                spider.logger.info(e)
                pass
            return item
        else:
            tmp = dict(item)
            del tmp["flag"]
            spider.logger.info("pipeline tmp {}".format(tmp))
            proxy=Proxy.objects.filter(ip=item["ip"], port=item["port"])
            proxy.update(**tmp)
            spider.logger.info(proxy.first())

