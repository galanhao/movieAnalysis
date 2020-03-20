from django.conf.urls import url
from django.urls import re_path
from home import views

urlpatterns = [
    url(r"^$", views.index, name='index'),

    url(r"^movielist", views.movieList, name='movieList'),

    url(r"^scorecontrast", views.scoreContrast, name='scoreContrast'),



    url(r"^proxy", views.proxy, name='proxy'),



    re_path(r"^getmapdata/(?P<mothod>map|mapdis)/(?P<movie_id>\d+)$", views.getMapData, name="getMapData"),
    url(r"^index/$", views.clash, name="clash"),
    url(r"^chinamap/$", views.mapJson, name="mapJson"),
]