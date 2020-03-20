from django.contrib import admin
from movieManager.models import Viewer, Comment, Movie
from django.conf.locale.es import formats as es_formats
# Register your models here.


class ViewerAdmin(admin.ModelAdmin):
    list_display = ["id", "user_id", "city"]
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "comment_id", "content", "movie"]
    search_fields = ('comment_id', 'content', 'movie__movie_name')  # 搜索字段
class MovieAdmin(admin.ModelAdmin):
    es_formats.DATETIME_FORMAT = "d M Y H:i:s"
    fk_fields = ["movie_comment",]
    list_display = ["id", "movie_id", "movie_name", "release_time"]

admin.site.register(Viewer, ViewerAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Movie, MovieAdmin)
