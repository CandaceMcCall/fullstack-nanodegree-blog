#!/usr/bin/env python
#
# Post Model for database
#
# Blog project for Udacity Full Stack NanoDegree
# Student:  Candace McCall
# Date:  02/05/2017
#
import os
import jinja2

from google.appengine.ext import db
from User import User
from Comment import Comment
from Likes import Likes

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


#
#   Post entry
#
class Post(db.Model):
    """
    Post:   Blog post database object
    Args:
            db.Model: Google App Engine database model
    """
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    user_id = db.IntegerProperty(required=True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", post=self)

    def get_user_name(self):
        u = User.by_id(int(self.user_id))
        return u.name

    def get_number_likes(self):
        number_likes = Likes.all().filter('post_id = ',
                                          self.key().id()).count()
        if number_likes:
            return number_likes
        else:
            return '0'

    def get_number_comments(self):
        number_comments = Comment.all().filter(
            'post_id = ', self.key().id()).count()
        if number_comments:
            return number_comments
        else:
            return '0'

    def is_liked_by_user(self, current_user_id):
        n = Likes.all().filter('post_id = ',
                               self.key().id()).filter('user_id = ',
                                                       int(current_user_id)).count()
        if n > 0:
            return 'Liked'
        else:
            return 'Like'
