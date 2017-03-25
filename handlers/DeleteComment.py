#!/usr/bin/env python
#
# DeleteComment BlogHandler
#
# Blog project for Udacity Full Stack NanoDegree
# Student:  Candace McCall
# Date:  02/05/2017
#
from handlers import BlogHandler
from models import User, Post, Comment, Likes
from google.appengine.ext import db
from blogsutil import blog_key
from errorcheck import user_owns_comment
from errorcheck import comment_exists
from errorcheck import user_logged_in


#
#   Delete Comment Page for Blog
#
class DeleteComment(BlogHandler):
    """
    DeleteComment:   Delete Comment
    Args:
            BlogHandler:     Blog Handler
    """
    @user_logged_in
    @comment_exists
    @user_owns_comment
    def get(self, comment_id):
        """
        get:   Get
        Args:
                self:   This object
                comment_id:    Comment ID
        """
        c = Comment.get_by_id(int(comment_id), parent=blog_key())

        if not c:
            self.render('notfound.html')
            return
#
#       Check that user IDs match
#
        user_id = self.user.key().id()
        if c.user_id != user_id:
            self.redirect('/blog/comment/%s' % str(c.key().id()))

        content = c.content
        self.render('deletecomment.html', content=content,
                    comment_id=comment_id)

    @user_logged_in
    @comment_exists
    @user_owns_comment
    def post(self, comment_id):
        """
        post:   Post
        Args:
                self:   This object
                comment_id:    Comment ID
        """
        if not self.user:
            return self.redirect('/login')

        c = Comment.get_by_id(int(comment_id), parent=blog_key())
#
#       Check that user IDs match
#
        user_id = self.user.key().id()
        if c.user_id != user_id:
            return self.redirect('/blog/comment/%s' % str(c.key().id()))
        c.delete()
        comments = Comment.all().filter('comment_id =', comment_id)
        for comment in comments:
            comment.delete()

        self.redirect('/blog/commentdeleted')
