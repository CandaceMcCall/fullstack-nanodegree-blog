#!/usr/bin/env python
#
# Blogs Utility functions
#
# Blog project for Udacity Full Stack NanoDegree
# Student:  Candace McCall
# Date:  02/05/2017
#
from google.appengine.ext import db


#
#   Blog key
#
def blog_key(name='default'):
    return db.Key.from_path('blogs', name)
