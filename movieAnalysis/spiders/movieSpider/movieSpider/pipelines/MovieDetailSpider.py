from movieManager.models import Person, Category, Movie
from spiders.movieSpider.movieSpider.spiders.maoYan_movie_detail import MaoyanMovieDetailSpider


class Pipeline(object):
    def process_item(self, item, spider):
        if spider.name == MaoyanMovieDetailSpider.name:
            movie = Movie.objects.filter(movie_id=item["movie_id"]).first()
            if movie:
                movie.introduce = item["introduce"]
                # TODO... 添加Awards
                for award in item["awards"]:
                    atmp = movie.awards.filter(awards_name=award["awards_name"]) \
                        .first()
                    if not atmp:
                        awardTmp = Awards.objects.create(**award)
                        movie.awards.add(awardTmp)
                # TODO... 添加 各类Person
                for person_tup in list(item["persons"].items()):
                    #   添加演员  Actor
                    # print(person_tup)
                    if person_tup[0] == "actor":
                        # print("actor")
                        for person in person_tup[1]:
                            ptmp = Person.objects.filter(user_id=person[1]).first()
                            if not ptmp:
                                personTmp = Person.objects.create(user_id=person[1])
                                movie.actor.add(personTmp)
                    #   添加导演 lead_director
                    elif person_tup[0] == "lead_director":
                        # print("lead_director")
                        for person in person_tup[1]:
                            ptmp = Person.objects.filter(user_id=person[1]).first()
                            if not ptmp:
                                personTmp = Person.objects.create(user_id=person[1])
                                movie.lead_director.add(personTmp)
                    #   添加副导演 vice_director
                    elif person_tup[0] == "vice_director":
                        # print("vice_director")
                        for person in person_tup[1]:
                            ptmp = Person.objects.filter(user_id=person[1]).first()
                            if not ptmp:
                                personTmp = Person.objects.create(user_id=person[1])
                                movie.vice_director.add(personTmp)

                # TODO... 添加分类
                for category in item["categorys"]:
                    cateTmp = Category.objects.filter(name=category).first()
                    if not cateTmp:
                        # print("创建",category)
                        categoryTmp = Category.objects.create(name=category)
                        movie.category.add(categoryTmp)

                    # 如果存在该分类，则查有没有该关联
                    else:
                        categoryTmp = movie.category.filter(name=category).first()
                        if not categoryTmp:
                            movie.category.add(cateTmp)

                movie.save()
        return item