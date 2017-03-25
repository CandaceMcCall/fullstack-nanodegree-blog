#!/usr/bin/env python
#
# LikePost Handler
#
# Blog project for Udacity Full Stack NanoDegree
# Student:  Candace McCall
# Date:  02/05/2017
#


from handlers import BlogHandler
from models import User, Post, Comment, Likes
from google.appengine.ext import db
from blogsutil import blog_key
from errorcheck import post_exists
from errorcheck import user_logged_in


#
#   Like Post Page for Blog
#
class LikePost(BlogHandler):
    """
    LikePost:   Like Post
    Args:
            BlogHandler:     Blog Handler
    """
    @user_logged_in
    @post_exists
    def get(self, post_id):
        """
        get:   Get
        Args:
                self:   This object
                post_id:    Post ID
        """
        if not self.user:
            return self.redirect('/login')

        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        b = db.get(key)

        if not b:
            self.render('notfound.html')
            return
#
#       Check that user IDs do not match
#
        user_id = self.user.key().id()
        if b.user_id == user_id:
            return self.redirect('/blog/%s' % str(b.key().id()))

        if b.is_liked_by_user(user_id) == 'Liked':
            return self.redirect('/blog/%s' % str(b.key().id()))

        l = Likes(parent=blog_key(), post_id=int(post_id),
                  user_id=int(user_id))
        l.put()
        self.redirect('/blog/%s' % str(b.key().id()))
