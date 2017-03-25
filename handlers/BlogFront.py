#!/usr/bin/env python
#
# BlogFront Handler
#
# Blog project for Udacity Full Stack NanoDegree
# Student:  Candace McCall
# Date:  02/05/2017
#


from handlers import BlogHandler
from models import User, Post
from google.appengine.ext import db
from blogsutil import blog_key


#
#   Blog Front Page for Blog
#
class BlogFront(BlogHandler):
    """
    BlogFront:   Blog Front Page
    Args:
            BlogHandler:     Blog Handler
    """
    def get(self):
        """
        get:   Get
        Args:
                self:   This object
        """
        entries = Post.all().order('-created')
        self.render("front.html", posts=entries)
