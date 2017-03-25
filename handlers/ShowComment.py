#!/usr/bin/env python
#
# ShowComment Blog Handler
#
# Blog project for Udacity Full Stack NanoDegree
# Student:  Candace McCall
# Date:  02/05/2017
#


from handlers import BlogHandler
from models import User, Post, Comment
from google.appengine.ext import db
from blogsutil import blog_key


#
#   Show Comment Class for Blog
#
class ShowComment(BlogHandler):
    """
    ShowPost:   Show Comment
    Args:
            BlogHandler:     Blog Handler
    """
    def get(self, comment_id):
        """
        get:   Get
        Args:
                self:   This object
        """
        key = db.Key.from_path('Comment', int(comment_id), parent=blog_key())
        comment = db.get(key)

        if not comment:
            self.render('notfound.html')
            return

        self.render('showcomment.html', comment=comment)
