# -*- coding: utf-8 -*-
import scrapy

from movieManager.models import Person
from spiders.movieSpider.movieSpider.items import PersonItem


class MaoyanPersonSpider(scrapy.Spider):
    name = 'maoYan_person'
    allowed_domains = ['maoyan.com']
    # start_urls = ['http://maoyan.com/']
    url_format = "https://maoyan.com/films/celebrity/{}"

    def start_requests(self):
        persons = Person.objects.filter(name="")
        for person in persons:
            print(person)
            yield scrapy.Request(url=self.url_format.format(person.user_id), meta={
                "user_id": person.user_id
            })

    def parse(self, response):
        item = PersonItem()

        item["user_id"] = None
        item["user_id"] = response.meta["user_id"]

        item["introduce"] = None
        item["introduce"] = response.xpath('//p[@class="cele-desc"]/text()').extract_first("").strip()

        item["name"] = None
        item["name"] = response.xpath('//p[@class="china-name cele-name"]/text()').extract_first("").strip()

        item["foreign_name"] = None
        item["foreign_name"] = response.xpath('//p[@class="eng-name cele-name"]/text()').extract_first("").strip()

        item["birth_place"] = None
        item["gender"] = None
        item["national"] = None
        item["nationality"] = None
        item["identity"] = None
        basicInfo_names = response.xpath('//dt[@class="basicInfo-item name"]/text()').extract()
        basicInfo_values = response.xpath('//dd[@class="basicInfo-item value"]/text()').extract()
        targets = [("birth_place", "出生地"),
                   ("gender", "性别"),
                   ("national", "名族"),
                   ("nationality", "国籍"),
                   ("identity", "身份"), ]
        info_names = []
        for basicInfo_name in basicInfo_names:
            info_names.append(basicInfo_name.strip().replace("\xa0", ""))
        # print(info_names)
        info_values = []
        for basicInfo_value in basicInfo_values:
            info_values.append(basicInfo_value.strip())
        if len(info_values) == len(info_names):
            for tag in targets:
                if tag[1] in info_names:
                    item[tag[0]] = info_values[info_names.index(tag[1])]
        if item["identity"]:
            tmp = item["identity"]
            item["identity"] = [x.strip() for x in tmp.split("|")]
        print(item)
        yield item



