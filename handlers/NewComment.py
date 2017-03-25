#!/usr/bin/env python
#
# NewComment Handler
#
# Blog project for Udacity Full Stack NanoDegree
# Student:  Candace McCall
# Date:  02/05/2017
#
import os

import jinja2
import webapp2

from handlers import BlogHandler
from models import User, Post, Comment
from google.appengine.ext import db
from blogsutil import blog_key


#
#   New Comment
#
class NewComment(BlogHandler):
    """
    NewComment:   New Comment
    Args:
            BlogHandler:     Blog Handler
    """
    def get(self, post_id):
        """
        get:   Get
        Args:
                self:   This object
                post_id:    Post ID
        """
        if self.user:
            self.render("newcomment.html", post_id=post_id)
        else:
            self.redirect("/login")

    def post(self, post_id):
        """
        post:   Post
        Args:
                self:   This object
                post_id:    Post ID
        """
        if not self.user:
            return self.redirect('/login')

        content = self.request.get("content")
        user_id = self.user.key().id()

        if content:
            c = Comment(parent=blog_key(), content=content,
                        post_id=int(post_id), user_id=user_id)
            c.put()
            self.redirect('/blog/%s' % str(post_id))
        else:
            error = "content, please!"
            self.render("newcomment.html", content=content, error=error)
