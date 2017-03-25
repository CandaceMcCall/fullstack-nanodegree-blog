#!/usr/bin/env python
#
# EditPost Handler
#
# Blog project for Udacity Full Stack NanoDegree
# Student:  Candace McCall
# Date:  02/05/2017
#


from handlers import BlogHandler
from models import User, Post
from google.appengine.ext import db
from blogsutil import blog_key
from errorcheck import user_owns_post
from errorcheck import post_exists
from errorcheck import user_logged_in


#
#   Edit Post Page for Blog
#
class EditPost(BlogHandler):
    """
    EditPost:   Edit Post
    Args:
            BlogHandler:     Blog Handler
    """
    @user_logged_in
    @post_exists
    @user_owns_post
    def get(self, post_id):
        """
        get:   Get
        Args:
                self:   This object
        """
        b = Post.get_by_id(int(post_id), parent=blog_key())

        if not b:
            self.render('notfound.html')
            return
#
#       Check that user IDs match
#
        user_id = self.user.key().id()
        if b.user_id != user_id:
            self.redirect('/blog/%s' % str(b.key().id()))

        subject = b.subject
        content = b.content
        self.render('editpost.html', subject=subject, content=content,
                    post_id=post_id)

    @user_logged_in
    @post_exists
    @user_owns_post
    def post(self, post_id):
        """
        post:   Post
        Args:
                self:   This object
                post_id:    Post ID
        """
        if not self.user:
            return self.redirect('/login')

        b = Post.get_by_id(int(post_id), parent=blog_key())
#
#       Check that user IDs match
#
        user_id = self.user.key().id()
        if b.user_id != user_id:
            return self.redirect('/blog/%s' % str(b.key().id()))

        subject = self.request.get("subject")
        content = self.request.get("content")

        if subject and content:
            b.subject = subject
            b.content = content
            b.put()
            self.redirect('/blog/%s' % str(b.key().id()))
        else:
            error = "subject and content, please!"
            self.render("editpost.html", subject=subject, content=content,
                        error=error)
