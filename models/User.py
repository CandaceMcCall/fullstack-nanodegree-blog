#!/usr/bin/env python
#
# User Model for database
#
# Blog project for Udacity Full Stack NanoDegree
# Student:  Candace McCall
# Date:  02/05/2017
#
import os
import random
import hashlib
from string import letters
from google.appengine.ext import db


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
