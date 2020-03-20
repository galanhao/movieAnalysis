from movieManager.models import Movie
from spiders.movieSpider.movieSpider.spiders.maoYan_movie import MaoyanMovieSpider


class Pipeline(object):
    def __updatePOP(self, model, data):
        try:
            data.pop("event")
        except:
            pass
        model.update(**data)
        # print(data, "update 成功")

    def __createPOP(self, model, data):
        try:
            data.pop("event")
        except:
            pass
        model.create(**data)
        # print(data, "create 成功")

    def process_item(self, item, spider):

        if spider.name == MaoyanMovieSpider.name:

            movie = Movie.objects.filter(movie_id=item["movie_id"])
            movie_data = dict(item)
            # print(movie_data)
            if movie:
                print("更新， ", movie_data)
                self.__updatePOP(movie, movie_data)
            else:
                print("创建， ", movie_data)
                self.__createPOP(movie, movie_data)
        return item