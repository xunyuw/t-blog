from tornado.web import authenticated
from base import BaseHandler
from models import post, tag, category

from datetime import datetime
from markdown import markdown


class AddHandler(BaseHandler):
    @authenticated
    def get(self):
        self.render("post_add.html", tags=tag.get_tags(), categories=category.get_categories())

    @authenticated
    def post(self):
        my_post = post.Post()
        my_post.title = self.get_argument("title")
        my_post.content = self.get_argument("content")
        my_post.category_id = int(self.get_argument("category"))
        for tag_item in tag.get_tags_by_ids(self.get_arguments("tags")):
            my_post.tags.append(tag_item)
        my_post.post_time = datetime.now()
        post.add(my_post)
        self.redirect("/admin/posts")


class ListHandler(BaseHandler):
    @authenticated
    def get(self):
        self.render("post_list.html", headers=post.get_headers())


class ShowHandler(BaseHandler):
    def get(self, id):
        my_post = post.get_post_by_id(int(id))
        my_post.content = markdown(my_post.content)
        self.render("post.html", post=post.get_post_by_id(int(id)))


class EditHandler(BaseHandler):
    @authenticated
    def get(self, id):
        my_post = post.get_post_by_id(int(id))
        selected_tags = [i.id for i in my_post.tags]
        self.render("post_edit.html", post=my_post, tags=tag.get_tags(), selected_tags=selected_tags, categories=category.get_categories())

    @authenticated
    def post(self, post_id):
        my_post = post.get_post_by_id(post_id)
        my_post.title = self.get_argument("title")
        my_post.content = self.get_argument("content")
        my_post.category_id = int(self.get_argument("category"))
        my_post.tags = []
        for tag_item in tag.get_tags_by_ids(self.get_arguments("tags")):
            my_post.tags.append(tag_item)
        post.update()
        self.redirect("/admin/posts")


class DeleteHandler(BaseHandler):
    @authenticated
    def get(self, post_id):
        self.render("post_delete.html", post=post.get_header_by_id(int(post_id)))

    @authenticated
    def post(self, post_id):
        post.delete_post_by_id(int(post_id))
        self.redirect("/admin/posts")
