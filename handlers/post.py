from tornado.web import RequestHandler
from models import post, tag, category

from datetime import datetime
from markdown import markdown
#from datetime.datetime import strftime


class AddPostHandler(RequestHandler):
    def get(self):
        self.render("post_add.html", tags=tag.get_tags(), categories=category.get_categories())

    def post(self):
        my_post = post.Post()
        my_post.title = self.get_argument("title")
        my_post.content = self.get_argument("content")
        my_post.category_id = int(self.get_argument("category"))
        for tag_item in tag.get_tags_by_ids(self.get_arguments("tags")):
            my_post.tags.append(tag_item)
        my_post.post_time = datetime.now()
        post.add(my_post)


class ListPostHandler(RequestHandler):
    def get(self):
        self.render("post_list.html")


class ShowPostHandler(RequestHandler):
    def get(self, id):
        my_post = post.get_post_by_id(int(id))
        my_post.content = markdown(my_post.content)
        self.render("post.html", post=post.get_post_by_id(int(id)))
