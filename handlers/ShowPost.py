#!/usr/bin/env python
#
# ShowPost Handler
#
# Blog project for Udacity Full Stack NanoDegree
# Student:  Candace McCall
# Date:  02/05/2017
#


from handlers import BlogHandler
from models import Post, Comment
from google.appengine.ext import db
from blogsutil import blog_key


#
#   Show Post Class for Blog
#
class ShowPost(BlogHandler):
    """
    ShowPost:   Show Post
    Args:
            BlogHandler:     Blog Handler
    """
    def get(self, post_id):
        """
        get:   Get
        Args:
                self:   This object
        """
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.render('notfound.html')
            return
#
#       Get comments
#
        comments = Comment.all().filter('post_id =', int(post_id))
        self.render('permalink.html', post=post, comments=comments)
