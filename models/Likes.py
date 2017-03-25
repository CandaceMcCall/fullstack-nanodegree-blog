#!/usr/bin/env python
#
# Likes Models for database
#
# Blog project for Udacity Full Stack NanoDegree
# Student:  Candace McCall
# Date:  02/05/2017
#
import os

from google.appengine.ext import db


#
#    Likes model
#
class Likes(db.Model):
    """
    Post:   Blog likes database object
    Args:
            db.Model: Google App Engine database model
    """
    post_id = db.IntegerProperty(required=True)
    user_id = db.IntegerProperty(required=True)
