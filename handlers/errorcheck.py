#!/usr/bin/env python
#
# Error Checks
#
# Blog project for Udacity Full Stack NanoDegree
# Student:  Candace McCall
# Date:  02/05/2017
#
import os

from models import User
from google.appengine.ext import db
from blogsutil import blog_key


#
#   Decorator function if check if user logged in
#
def user_logged_in(function):
    def wrapper(self, entity_id):
        if not self.user:
            self.redirect('/login')
            return
        else:
            return function(self, entity_id)
    return wrapper


#
#   Decorator function if check if post exists
#
def post_exists(function):
    def wrapper(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        if post:
            return function(self, post_id)
        else:
            self.render('notfound.html')
            return
    return wrapper


#
#   Decorator function if check if comment exists
#
def comment_exists(function):
    def wrapper(self, comment_id):
        key = db.Key.from_path('Comment', int(comment_id),
                               parent=blog_key())
        comment = db.get(key)
        if comment:
            return function(self, comment_id)
        else:
            self.render('notfound.html')
            return
    return wrapper


#
#    Decorator function to check if user owns post
#
def user_owns_post(function):
    def wrapper(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        if self.user.key().id() == post.user_id:
            return function(self, post_id)
        else:
            self.redirect('/')
            return
    return wrapper


#
#    Decorator function to check if user owns comment
#
def user_owns_comment(function):
    def wrapper(self, comment_id):
        key = db.Key.from_path('Comment', int(comment_id),
                               parent=blog_key())
        comment = db.get(key)
        if self.user.key().id() == comment.user_id:
            return function(self, comment_id)
        else:
            self.redirect('/')
            return
    return wrapper
