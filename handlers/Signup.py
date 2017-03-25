#!/usr/bin/env python
#
# Signup Handler
#
# Blog project for Udacity Full Stack NanoDegree
# Student:  Candace McCall
# Date:  02/05/2017
#


import re
from handlers import BlogHandler


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")


#
#   Helper functions for checking for valid fields in signup form
#
def valid_username(username):
    return USER_RE.match(username)


def valid_password(password):
    return PASSWORD_RE.match(password)


def valid_email(email):
    return not email or EMAIL_RE.match(email)


#
#   Signup Handler class
#
class Signup(BlogHandler):
    """
    Signup:   Handler for signup
    Args:
            BlogHandler:     Blog Handler
    """
    def get(self):
        """
        get:   Get
        Args:
                self:   This object
        """
        self.render("signup.html")

    def post(self):
        """
        post:   Post
        Args:
                self:   This object
        """
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify_password = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username=self.username, email=self.email)

        error_encountered = False
        if not valid_username(self.username):
            params['username_error'] = "That's not a valid username."
            error_encountered = True

        if not valid_password(self.password):
            params['password_error'] = "That wasn't a valid password."
            error_encountered = True
        elif self.password != self.verify_password:
            params['verify_password_error'] = "Your passwords didn't match."
            error_encountered = True

        if not valid_email(self.email):
            params['email_error'] = "That's not a valid email."
            error_encountered = True

        if error_encountered:
            self.render("signup.html", **params)
        else:
            self.done()

    def done(self, *a, **kw):
        """
        done:   Done (Not implemented)
        Args:
                self:  This object
                *a:
                **kw:
        """
        raise NotImplementedError
