#!/usr/bin/env python
#
# DeletePost BlogHandler
#
# Blog project for Udacity Full Stack NanoDegree
# Student:  Candace McCall
# Date:  02/05/2017
#


from handlers import BlogHandler
from models import User, Post, Comment, Likes
from google.appengine.ext import db
from blogsutil import blog_key
from errorcheck import user_owns_post
from errorcheck import post_exists
from errorcheck import user_logged_in


#
#   Delete Post Page for Blog
#
class DeletePost(BlogHandler):
    """
    DeletePost:   Delete Post
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
                post_id:    Post ID
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
        self.render('deletepost.html', subject=subject, content=content,
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
        b.delete()
        comments = Comment.all().filter('post_id =', post_id)
        for comment in comments:
            comment.delete()

        self.redirect('/blog/postdeleted')
