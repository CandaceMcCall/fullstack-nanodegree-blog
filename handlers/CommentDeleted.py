#!/usr/bin/env python
#
# CommentDeleted BlogHandler
#
# Blog project for Udacity Full Stack NanoDegree
# Student:  Candace McCall
# Date:  02/05/2017
#
import os

import jinja2
import webapp2
import re
import hmac

from handlers import BlogHandler
from models import User, Post, Comment, Likes
from google.appengine.ext import db


#
#    Comment Deleted Class
#
class CommentDeleted(BlogHandler):
    """
    CommentDeleted:   Comment Deleted Class
    Args:
            BlogHandler:     Blog Handler
    """
    def get(self):
        """
        get:   Get
        Args:
                self:   This object
        """
        if self.user:
            self.render('commentdeleted.html')
        else:
            self.redirect('/login')
