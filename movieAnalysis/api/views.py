from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

import numpy as np

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from movieManager.models import Movie, Viewer, Person, Comment, Category

def myCustomSQL(sql):
    row = None
    with connection.cursor() as cursor:
        cursor.execute(sql)
        row = cursor.fetchall()
    return row


# CBV比较特殊，不能单独加在某个方法上
# 只能加在类上或dispatch方法上
@method_decorator(csrf_exempt, name='dispatch')
class GetOverviewView(View):
    def get(self, request):
        viewer = {
            "overview": Viewer.objects.count(),
            "label": ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期天"],
            "value": [23, 56, 85, 90, 85, 12, 33],
        }
        movie = {
            "overview": Movie.objects.count(),
            "label": ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期天"],
            "value": [23, 56, 85, 50, 20, 12, 33],
        }
        comment = {
            "overview": Comment.objects.count(),
            "label": ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期天"],
            "value": [23, 56, 85, 50, 20, 12, 33],
        }
        category = {
            "overview": Category.objects.count(),
            "label": ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期天"],
            "value": [23, 56, 85, 50, 20, 12, 33],
        }


        res = {
            "viewer": viewer,
            "movie": movie,
            "comment": comment,
            "category": category
        }
        return JsonResponse(res)

    def post(self, request):
        return HttpResponse("A")

@method_decorator(csrf_exempt, name='dispatch')
class GetTopTable1(View):
    def getMovieListByCommentNum(self):
        sql = 'select '\
                  'm.id,'\
                  'm.release_time, '\
                  'm.movie_id, '\
                  'm.movie_name,'\
                  'm.score,'\
                  'c.dx '\
            'from '\
              'moviemanager_movie as m, '\
              '(select movie_id, count(*) as \'dx\' from moviemanager_comment group by movie_id) as c '\
            'where c.movie_id=m.id order by c.dx DESC limit 10;'
        rs = myCustomSQL(sql)
        return rs

    def get(self, request):
        rs = self.getMovieListByCommentNum()
        # print(rs)
        ret = {"data": rs}
        return JsonResponse(ret)

@method_decorator(csrf_exempt, name='dispatch')
class GetTopTable2(View):
    def get(self, request):
        movies = Movie.objects.values("movie_name", "score").order_by("-score")[:10]
        res = {"data": list(movies)}
        return JsonResponse(res)

@method_decorator(csrf_exempt, name='dispatch')
class GetMovieList1(View):
    def getMovieList1(self, start, size=15):
        sql = 'select ' \
              'm.id,' \
              'm.release_time, ' \
              'm.movie_id, ' \
              'm.movie_name,' \
              'm.score,' \
              'c.dx ' \
              'from ' \
              'moviemanager_movie as m, ' \
              '(select movie_id, count(*) as \'dx\' from moviemanager_comment group by movie_id) as c ' \
              'where c.movie_id=m.id order by m.score DESC limit %d,%d;'%(start, size)
        # (0,5)1,2,3,4,5   (5,5)6,,7,8,9,10
        rs = myCustomSQL(sql)
        return rs

    def get(self, request):
        num= 1
        try:
            num = int(request.GET.get("pageIndex"))
        except BaseException as e:
            print(e)
        rs = self.getMovieList1((num-1)*15)
        ret = {"data":rs}
        d_category = []
        for c in rs:
            mTmp = Movie.objects.filter(id=c[0]).first().category.values("name").all()
            tmp = []
            for v in mTmp:
                tmp.append(v["name"])
            d_category.append(tmp)
        ret["d_category"] = d_category
        return JsonResponse(ret)


class GetMovieList2(View):
    def get(self, request):
        num = 1
        size = 15
        try:
            num = int(request.GET.get("pageIndex"))
            num = max(1, num)
        except BaseException as e:
            print(e)
        start = (num-1)*size
        end = start + size
        print(start, end)
        movies = Movie.objects.values("movie_id", "id", "movie_name").all()[start: end]

        res = {
            "movies": list(movies),
            "pageIndex": num,
            "size": size,
            "total": Movie.objects.count()
        }
        # print(res)
        return JsonResponse(res)


class GetScoreDistribution1(View):
    def get(self, request):

        # 其实是 Movie 的 ID，不是movie_id
        movie_id = -1
        try:
            movie_id = request.GET.get("movie_id")
            movie_id = int(movie_id)
        except:
            pass
        if movie_id==-1:
            return JsonResponse({})

        sql = 'select ' \
              'score, count(*) as \'dx\' ' \
              'from moviemanager_comment ' \
              'where movie_id={} ' \
              'group by score;'.format(movie_id)

        rs = myCustomSQL(sql)
        print(rs)
        labels = list(np.arange(0, 5.1, 0.5))
        values = []
        for label in labels:
            tmp = 0
            for r in rs:
                if r[0] == label:
                    tmp = r[1]
            values.append(tmp)
        ret = {
            # "label": labels,
            "value": values,
        }
        return JsonResponse(ret)


@method_decorator(csrf_exempt, name='dispatch')
class GetPersonList1(View):
    def getPersonList1(self, start, size=15):
        rs = []
        persons = Person.objects.exclude(name="")[start: start+size]
        for c in persons:
            tmp = {}
            print(c.id, c.name)
            print([x.name for x in c.identity.all()])
            tmp["name"] = c.name
            tmp["foreign_name"] = c.foreign_name
            tmp["uid"] = c.user_id
            tmp["nationality"] = c.nationality
            tmp["gender"] = c.gender
            tmp["identity"] = [x.name for x in c.identity.all()]
            rs.append(tmp)
        # print(len(persons))
        return rs

    def get(self, request):
        num= 1
        try:
            num = int(request.GET.get("pageIndex"))
        except BaseException as e:
            print(e)
        rs = self.getPersonList1((num-1)*15)
        ret = {
            "data": rs
        }
        return JsonResponse(ret)