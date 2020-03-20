from django.conf.urls import url
from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt

from api import views
urlpatterns = [
    # url(r"^getoverview$", csrf_exempt(views.GetOverviewView.as_view()), name='getOverview'),
    url(r"^getoverview/$", views.GetOverviewView.as_view(), name='getOverview'),
    url(r"^gettoptable1/$", views.GetTopTable1.as_view(), name='getTopTable1'),
    url(r"^gettoptable2/$", views.GetTopTable2.as_view(), name='GetTopTable2'),

    url(r"^getmovielist1/$", views.GetMovieList1.as_view(), name='GetMovieList1'),
    url(r"^getmovielist2/$", views.GetMovieList2.as_view(), name='GetMovieList2'),


    url(r"^getpersonlist1/$", views.GetPersonList1.as_view(), name='GetPersonList1'),


    url(r"^getscoredistribution1/$", views.GetScoreDistribution1.as_view(), name='GetScoreDistribution1'),



]