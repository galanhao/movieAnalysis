# -*- coding: utf-8 -*-
import datetime
import json

import scrapy

from spiders.movieSpider.movieSpider.items import CommentItem, ViewerItem


class MaoyanCommentSpider(scrapy.Spider):
    name = 'maoYan_comment'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://maoyan.com/']
    start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 如果end_time 等于 None，则没有结束时间，爬完为止
    # 如果有的话则爬到这个时间为止
    # end_time = datetime.datetime.strptime("2019-10-4 12:5:12", '%Y-%m-%d %H:%M:%S')
    end_time = None

    movie_id_list = [488, 790, 267, 4055, 1297]

    def start_requests(self):
        for c in self.movie_id_list:
            url = "http://m.maoyan.com/mmdb/comments/movie/{}.json?" \
                  "_v_=yes&offset={}&" \
                  "startTime={}"
            print(url.format(c, 0, self.start_time))
            offset = 0
            yield scrapy.Request(url=url.format(c, offset, self.start_time), meta={
                                        "url_format": url,
                                        "movie_id": c,
                                        "start_time": self.start_time,
                                        "offset": offset
                                    },
                                 callback=self.parseTransit,
                                 dont_filter=True)

    def parseResponse(self, response):
        # print("parse")
        if response and response.status == 200:
            datas = json.loads(response.body)["cmts"]
            flag, url_format, movie_id, offset, rp_start_time = \
                self.verifySUOM(dict(response.meta))
            zc_start_time = None
            for data in datas:
                comment = CommentItem()
                view = ViewerItem()
                view["user_id"] = data["userId"]
                view["user_level"] = data.get("userLevel", None)
                view["city"] = data.get("cityName", None)
                view["gender"] = data.get("gender", 0)
                view["vipInfo"] = data.get("vipInfo", "")
                view["vipType"] = data.get("vipType", 0)

                comment["movie"] = data["movieId"]
                comment["comment_id"] = data["id"]
                comment["start_time"] = datetime.datetime.strptime(data["startTime"], '%Y-%m-%d %H:%M:%S')
                zc_start_time = data["startTime"]
                comment["content"] = data["content"]
                comment["score"] = data["score"]
                comment["viewer"] = view
                # print("要yeild的comment", comment)
                yield comment

            def __changeStartTime():
                rp_start_time = zc_start_time
                # 如果早于结束时间
                if self.end_time == None or datetime.datetime.strptime(zc_start_time,
                                                                       '%Y-%m-%d %H:%M:%S') > self.end_time:
                    print("开始更改开始时间1", zc_start_time)
                    return scrapy.Request(url=url_format
                                          .format(movie_id,
                                                  0,
                                                  rp_start_time.replace(" ", "%20")),
                                          meta={
                                              "start_time": rp_start_time,
                                              "url_format": url_format,
                                              "offset": 0,
                                              "movie_id": movie_id
                                          },
                                          callback=self.parseTransit,
                                          dont_filter=True)
                else:
                    print("超过结束时间", self.end_time)

            if flag:
                if offset < 1000:
                    if len(datas) < 1:
                        pass  # 偏移没到1000，但是数据不满15，证明爬完了 现在是1
                        print("没有数据了，爬个毛")
                    else:
                        # TODO... 增加偏移量继续爬
                        offset += 15
                        if offset <= 1000:
                            yield scrapy.Request(url=url_format
                                                 .format(movie_id,
                                                         offset,
                                                         rp_start_time.replace(" ", "%20")),
                                                 meta={
                                                     "start_time": rp_start_time,
                                                     "url_format": url_format,
                                                     "offset": offset,
                                                     "movie_id": movie_id
                                                 },
                                                 dont_filter=True,
                                                 callback=self.parseTransit)
                        else:
                            yield __changeStartTime()
                else:
                    yield __changeStartTime()

    def verifySUOM(self, data):

        start_time = data.get("start_time", False)
        url_format = data.get("url_format", False)
        offset = data.get("offset", "wohuo")
        movie_id = data.get("movie_id", "wohuo")
        # TODO... 验证信息是否完整
        if not start_time or not url_format \
                or offset == "wohuo" or movie_id == "wohuo":
            return False, url_format, movie_id, offset, start_time
        return True, url_format, movie_id, offset, start_time

    def parseTransit(self, response):
        # print(response.meta)
        data = dict(response.meta)
        flag, url_format, movie_id, offset, start_time = self.verifySUOM(data)
        # print(flag, url_format, movie_id, offset, start_time)
        if flag:
            yield scrapy.Request(url=url_format.format(movie_id, offset, start_time.replace(" ", "%20")),
                                 meta={
                                     "start_time": start_time,
                                     "url_format": url_format,
                                     "offset": offset,
                                     "movie_id": movie_id
                                 },
                                 dont_filter=True,
                                 callback=self.parseResponse)
