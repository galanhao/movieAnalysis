# -*- coding: utf-8 -*-
import re

import scrapy

from movieManager.models import Movie
from spiders.movieSpider.movieSpider.items import MovieDetailItem


class MaoyanMovieDetailSpider(scrapy.Spider):
    name = 'maoYan_movie_detail'
    allowed_domains = ['maoyan.com']
    # start_urls = ['http://maoyan.com/']
    format_url = "https://maoyan.com/films/{}"
    def start_requests(self):
        # print("kais")
        # movies = Movie.objects.filter(introduce=None)
        movies = Movie.objects.all()
        # movies = Movie.objects.filter(movie_id=1221)[:30]
        for movie in movies:
            yield scrapy.Request(self.format_url.format(movie.movie_id),
                                 meta={
                                     "movie_id": movie.movie_id
                                 })

    def parse(self, response):
        # print(response)
        # print(response.body)

        introduce = response.xpath('//span[@class="dra"]/text()').extract_first("")

        # TODO... 获取奖项列表
        awards = self.getAwards(response)

        # TODO... 获取人物列表
        persons = self.getPerson(response)

        # TODO... 获取电影类别
        categorys = self.getCategory(response)

        # print(introduce)
        # print(awards)
        # print(persons)
        # print(categorys)
        item = MovieDetailItem()
        # item["event"] = "MovieDetailItem"
        item["movie_id"] = response.meta["movie_id"]
        item["introduce"] = introduce
        item["awards"] = awards
        item["persons"] = persons
        item["categorys"] = categorys
        yield item

    def getPerson(self, response):
        celebrity_list = response.xpath('//div[@class="celebrity-container"]/div')
        persons = {
            "actor": [],
            "lead_director": [],
            "vice_director": []
        }

        def __getPerson(lis):
            res = []
            for li in lis:
                url = li.xpath('a/@href').extract_first()
                id = re.findall('\d+', url)
                if len(id) < 1:
                    return None
                res.append((url, id[0]))
            # print(res, id[0])
            return res

        for celebrity in celebrity_list[:3]:
            ii = celebrity.xpath('div/text()').extract_first("").strip()
            if ii == "演员":
                pinfo = __getPerson(celebrity.xpath('ul/li'))
                persons["actor"] = pinfo
                # print("演员", pinfo)
            elif ii == "导演":
                pinfo = __getPerson(celebrity.xpath('ul/li'))
                persons["lead_director"] = pinfo
                # print("导演", pinfo)
            elif ii == "副导演":
                pinfo = __getPerson(celebrity.xpath('ul/li'))
                persons["vice_director"] = pinfo
                # print("副导演", pinfo)
        return persons

    def getAwards(self, response):
        awards = []
        award_lis = response.xpath('//*[@id="app"]/div/div[1]/div/div[3]/div[3]/ul/li')
        for li in award_lis:
            award_name = li.xpath('div[1]/text()').extract()[1].strip()
            award_method_tmp = li.xpath('div[@class="content"]/div')
            award_content = {"awards_name": award_name}
            for c in award_method_tmp:
                tmp = c.xpath("text()").extract_first("")
                prize_t = re.findall('获奖：(.*)', tmp)
                nominate_t = re.findall('提名：(.*)', tmp)
                if len(prize_t) > 0:
                    award_content["prize"] = prize_t[0]
                elif len(nominate_t) > 0:
                    award_content["nominate"] = nominate_t[0]
            awards.append(award_content)
        return awards

    def getCategory(self, response):
        categorys = []
        a_list = response.xpath('//div[@class="movie-brief-container"]//a')
        for a in a_list:
            categorys.append(a.xpath('text()').extract_first("").strip())
        # print(categorys)
        return categorys
