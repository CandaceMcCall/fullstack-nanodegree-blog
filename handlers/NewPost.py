#!/usr/bin/env python
#
# NewPost Handler
#
# Blog project for Udacity Full Stack NanoDegree
# Student:  Candace McCall
# Date:  02/05/2017
#


from handlers import BlogHandler
from models import Post
from google.appengine.ext import db
from blogsutil import blog_key


#
#   New Blog Post
#
class NewPost(BlogHandler):
    """
    NewPost:   New Post
    Args:
            BlogHandler:     Blog Handler
    """
    def get(self):
        """
        get:   Get
        Args:
                self:   This object
                post_id:    Post ID
        """
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect("/login")

    def post(self):
        """
        post:   Post
        Args:
                self:   This object
        """
        if not self.user:
            return self.redirect('/login')

        subject = self.request.get("subject")
        content = self.request.get("content")
        user_id = self.user.key().id()

        if subject and content:
            b = Post(parent=blog_key(), subject=subject, content=content,
                     user_id=user_id)
            b.put()
            self.redirect('/blog/%s' % str(b.key().id()))
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject=subject, content=content,
                        error=error)
