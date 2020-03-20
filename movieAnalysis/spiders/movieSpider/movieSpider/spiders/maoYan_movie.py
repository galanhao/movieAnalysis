# -*- coding: utf-8 -*-
import datetime
import re

import scrapy

from spiders.movieSpider.movieSpider.items import MovieItem


class MaoyanMovieSpider(scrapy.Spider):
    name = 'maoYan_movie'
    allowed_domains = ['maoyan.com']
    # start_urls = ['http://maoyan.com/']
    format_url = "https://maoyan.com/board/4?offset={}"  # 0  90
    datail_url = "https://maoyan.com/films/{}"

    def start_requests(self):
        for c in range(0, 101, 10):
            print("Ccccccccccccccc", c)
            url = self.format_url.format(c)
            print(url)
            yield scrapy.Request(url=url,
                                 callback=self.parseMovieList,
                                 dont_filter=True)
    def parseMovieList(self, response):
        # print(response.body)
        dds = response.xpath('//dl[@class="board-wrapper"]/dd')
        for dd in dds:
            movie_item =MovieItem()
            movie_name = dd.xpath('div/div/div[1]/p[@class="name"]/a/text()').extract_first(None)
            # print(movie_name)
            movie_item["movie_name"] = movie_name

            movie_id = None
            movie_id_tmp = dd.xpath('a/@href').extract_first(None)
            if movie_id_tmp:
                _movie_id_tmp = re.findall('/(\d+)', movie_id_tmp)
                if len(_movie_id_tmp)==1:
                    movie_id = int(_movie_id_tmp[0])
            # print(movie_id)
            movie_item["movie_id"] = movie_id

            lead_actor_tmp = dd.xpath('div/div/div[1]/p[@class="star"]/text()') \
                .extract_first("").strip()
            lead_actor = lead_actor_tmp.replace("主演：", "").split(",")
            # print(lead_actor)

            release_time_tmp = dd.xpath('div/div/div[1]/p[@class="releasetime"]/text()') \
                .extract_first("").strip()
            r1 = re.findall('(\d+)', release_time_tmp)
            r2 = re.findall('\((.*?)\)', release_time_tmp)
            release_time = None
            release_area = None
            if len(r1) != 0:
                release_time = r1
            if len(r2) != 0:
                release_area = r2[0]
            # print(release_time, release_area)
            print(release_time)
            if len(release_time) == 3:
                movie_item["release_time"] = datetime.date(
                    int(release_time[0]),
                    int(release_time[1]),
                    int(release_time[2]), )
            else:
                movie_item["release_time"] = datetime.date(1,1,1)

            movie_item["release_area"] = release_area

            score = None
            scores_tmp = dd.xpath('div/div/div[2]/p[@class="score"]/i')
            score_tmp = ""
            for i in scores_tmp:
                score_tmp += i.xpath('text()').extract_first("").strip()
            try:
                score = float(score_tmp)
            except:
                pass
            # print(score)
            movie_item["score"] = score
            movie_item["event"] = "MovieItem"
            # print(movie_item)
            yield movie_item