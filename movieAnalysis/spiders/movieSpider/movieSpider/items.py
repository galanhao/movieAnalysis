# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from movieManager.models import Movie

from movieManager.models import Awards
from movieManager.models import Person
from movieManager.models import Comment
from movieManager.models import Viewer

class CommentItem(DjangoItem):
    django_model = Comment

class ViewerItem(DjangoItem):
    django_model = Viewer

class MovieDetailItem(DjangoItem):
    event = scrapy.Field()
    movie_id = scrapy.Field()
    introduce = scrapy.Field()
    awards = scrapy.Field()
    persons = scrapy.Field()
    categorys = scrapy.Field()



class MovieItem(DjangoItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    django_model = Movie
    event = scrapy.Field()

class AwardsItem(DjangoItem):
    django_model = Awards

class PersonItem(DjangoItem):
    django_model = Person
    identity = scrapy.Field()



