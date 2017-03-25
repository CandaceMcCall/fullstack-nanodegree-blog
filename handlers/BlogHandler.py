#!/usr/bin/env python
#
# BlogHandler
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

from models import User
from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
#
#   Helper functions to for hashing in setting cookies
#
SECRET = "mysecretcode!"


def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()


def make_secure_val(val):
    return '%s|%s' % (val, hash_str(val))


def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val


def users_key(group='default'):
    return db.Key.from_path('users', group)


#
#   Helper functions for checking for valid fields in signup form
#
def valid_username(username):
    return USER_RE.match(username)


def valid_password(password):
    return PASSWORD_RE.match(password)


def valid_email(email):
    return not email or EMAIL_RE.match(email)


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


#
#   Blog Handler class
#
class BlogHandler(webapp2.RequestHandler):
    """
    BlogHandler:   Handler for blog
    Args:
            webapp2.RequestHandler:     Webapp2 Request Handler
    """
    def write(self, *a, **kw):
        """
        write:   Write response
        Args:
                *a:
                **kw:
        """
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        """
        render_str:  Render string
        Args:
                self:       This object
                template:   Template
                **params:   Parameters
        Returns:
                template
        """
        params['user'] = self.user
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        """
        render:    Render template
        Args:
                self:       This object
                template:   Template
                **kw:       kw
        """
        self.write(self.render_str(template, **kw))

    #
    # Method to set cookie in header
    #
    def set_secure_cookie(self, name, val):
        """
        set_secure_cookie:  Set secure cookie
        Args:
                self:       This object
                name:       Cookie name
                val:        Cookie value
        """
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    #
    # Method to get cookie from header
    #
    def read_secure_cookie(self, name):
        """
        read_secure_cookie:  Read secure cookie
        Args:
                self:       This object
                name:       Cookie name
        """
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        """
        login:  Login
        Args:
                self:       This object
                user:       User object
        """
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        """
        logout:  Logout
        Args:
                self:       This object
        """
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        """
        initialize:   Initialize
        Args:
                *a:
                **kw:
        """
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))
