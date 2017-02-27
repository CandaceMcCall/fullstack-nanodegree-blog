#!/usr/bin/env python
#
# Models for database
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

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


#
#   Helper functions for making hash passwords to store in column
#   in User table in database
#
def make_salt(length=5):
    return ''.join(random.choice(letters) for x in xrange(length))


def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)


def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)


def users_key(group='default'):
    return db.Key.from_path('users', group)


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


#
#   User class for User object
#
class User(db.Model):
    """
    User:   User database object
    Args:
            db.Model: Google App Engine database model
    """
    name = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        """
        by_id:   Get User object by ID
        Args:
                 cls:    Class
                 uid:    User ID
        Returns:
                 return User object
        """
        return cls.get_by_id(uid, parent=users_key())

    @classmethod
    def by_name(cls, name):
        """
        by_name:   Get User object by ID
        Args:
                 cls:    Class
                 name:   User Name
        Returns:
                 return User object
        """
        u = cls.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email=None):
        """
        register:   Get User object by ID
        Args:
                 cls:    Class
                 name:   User Name
                 pw:     Password
                 email:  Email (default to None)
        Returns:
                 return User object
        """
        pw_hash = make_pw_hash(name, pw)
        return User(parent=users_key(),
                    name=name,
                    pw_hash=pw_hash,
                    email=email)

    @classmethod
    def login(cls, name, pw):
        """
        login:   Get User object by ID
        Args:
                 cls:    Class
                 uid:    User ID
        Returns:
                 return User object
        """
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u


#
#   Post entry
#
class Post(db.Model):
    """
    Post:   Blog post database object
    Args:
            db.Model: Google App Engine database model
    """
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    user_id = db.IntegerProperty(required=True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", post=self)

    def get_user_name(self):
        u = User.by_id(int(self.user_id))
        return u.name

    def get_number_likes(self):
        number_likes = Likes.all().filter('post_id = ',
                                          self.key().id()).count()
        if number_likes:
            return number_likes
        else:
            return '0'

    def get_number_comments(self):
        number_comments = Comment.all().filter(
            'post_id = ', self.key().id()).count()
        if number_comments:
            return number_comments
        else:
            return '0'

    def is_liked_by_user(self, current_user_id):
        n = Likes.all().filter('post_id = ',
                               self.key().id()).filter('user_id = ',
                                                       current_user_id).count()
        if n > 0:
            return 'Liked'
        else:
            return 'Like'


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
