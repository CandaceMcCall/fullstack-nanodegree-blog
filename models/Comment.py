#!/usr/bin/env python
#
# Comment Model for database
#
# Blog project for Udacity Full Stack NanoDegree
# Student:  Candace McCall
# Date:  02/05/2017
#
import os
import jinja2
import random
import hashlib
from string import letters

from google.appengine.ext import db
from User import User

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


#
# Comment data model
#
class Comment(db.Model):
    """
    Post:   Blog comment database object
    Args:
            db.Model: Google App Engine database model
    """
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    post_id = db.IntegerProperty(required=True)
    user_id = db.IntegerProperty(required=True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("comment.html", comment=self)

    def get_user_name(self):
        u = User.by_id(int(self.user_id))
        return u.name
