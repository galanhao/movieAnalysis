from movieManager.models import Comment, Movie, Viewer
from spiders.movieSpider.movieSpider.spiders.maoYan_comment import MaoyanCommentSpider


class Pipeline(object):

    def process_item(self, item, spider):
        #  处理 MovieCommentSpider的管道
        # print("处理 MovieCommentSpider的管道")
        if spider.name == MaoyanCommentSpider.name:
            # print(spider.name, MaoyanCommentSpider.name)
            #  TODO... 处理 viewer

            # print("TODO... 处理 viewer", item)
            viewerItem = item["viewer"]
            viewer = Viewer.objects.filter(user_id=viewerItem["user_id"])
            viewer_dict = dict(viewerItem)
            # print("viewer_dict", viewer_dict)
            if viewer.first():
                # print("update viewer")
                viewer.update(**viewer_dict)
                viewer = viewer.first()
            else:
                # print("create viewer")
                viewer = Viewer.objects.create(**viewer_dict)
                viewer = Viewer.objects.filter(**viewer_dict).first()

            # TODO... 检查Movie是否存在
            # print("TODO... 检查Movie是否存在")
            movie = Movie.objects.filter(movie_id=item["movie"])
            if movie.first():

                item_tmp = item
                item_tmp["movie"] = movie.first()
                item_tmp["viewer"] = viewer
                item_tmp_dict = dict(item_tmp)
                # print("item_tmp_dict", item_tmp_dict)
                comment = Comment.objects.filter(comment_id=item_tmp["comment_id"])
                if comment:
                    # print("update comment")
                    comment.update(**item_tmp_dict)
                    comment = comment.first()
                else:
                    # print("create comment")
                    Comment.objects.create(**item_tmp_dict)
                    comment = Comment.objects.filter(**item_tmp_dict).first()

        # print(item)

        return item