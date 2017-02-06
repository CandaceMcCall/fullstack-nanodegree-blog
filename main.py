#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
import random
import hashlib
from string import letters

from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
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
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        params['user'] = self.user
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    #
    # Method to set cookie in header
    #
    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    #
    # Method to get cookie from header
    #
    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))


#
#   Signup Handler class
#
class Signup(BlogHandler):
    def get(self):
        self.render("signup.html")

    def post(self):
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
        raise NotImplementedError


#
#   Login class
#
class Login(BlogHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/welcome')
        else:
            msg = 'Invalid login'
            self.render('login.html', login_error=msg)


#
#   Logout class
#
class Logout(BlogHandler):
    def get(self):
        self.logout()
        self.redirect('/signup')


class Register(Signup):
    def done(self):
        #
        # check if user already exists
        #
        u = User.by_name(self.username)
        if u:
            msg = 'That user already exists.'
            self.render('signup.html', username_error=msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()

            self.login(u)
            self.redirect('/welcome')


#
#    Welcome Class
#
class Welcome(BlogHandler):
    def get(self):
        if self.user:
            self.render('welcome.html', username=self.user.name)
        else:
            self.redirect('/signup')


#
#    Post Deleted Class

class PostDeleted(BlogHandler):
    def get(self):
        if self.user:
            self.render('postdeleted.html')
        else:
            self.redirect('/blog')


#
#   Blog Front Page for Blog
#
class BlogFront(BlogHandler):
    def get(self):
        entries = Post.all().order('-created')
        self.render("front.html", posts=entries)


#
#   Show Post Class for Blog
#
class ShowPost(BlogHandler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return
#
#       Get comments
#
        comments = Comment.all().filter('post_id =', int(post_id))
        self.render('permalink.html', post=post, comments=comments)


#
#   Edit Post Page for Blog
#
class EditPost(BlogHandler):
    def get(self, post_id):
        b = Post.get_by_id(int(post_id), parent=blog_key())

        if not b:
            self.error(404)
            return
#
#       Check that user IDs match
#
        user_id = self.user.key().id()
        if b.user_id != user_id:
            self.redirect('/blog/%s' % str(b.key().id()))

        subject = b.subject
        content = b.content
        self.render('editpost.html', subject=subject, content=content,
                    post_id=post_id)

    def post(self, post_id):
        if not self.user:
            self.redirect('/blog')

        b = Post.get_by_id(int(post_id), parent=blog_key())
        subject = self.request.get("subject")
        content = self.request.get("content")

        if subject and content:
            b.subject = subject
            b.content = content
            b.put()
            self.redirect('/blog/%s' % str(b.key().id()))
        else:
            error = "subject and content, please!"
            self.render("editpost.html", subject=subject, content=content,
                        error=error)


#
#   Delete Post Page for Blog
#
class DeletePost(BlogHandler):
    def get(self, post_id):
        b = Post.get_by_id(int(post_id), parent=blog_key())

        if not b:
            self.error(404)
            return
#
#       Check that user IDs match
#
        user_id = self.user.key().id()
        if b.user_id != user_id:
            self.redirect('/blog/%s' % str(b.key().id()))

        subject = b.subject
        content = b.content
        self.render('deletepost.html', subject=subject, content=content,
                    post_id=post_id)

    def post(self, post_id):
        if not self.user:
            self.redirect('/blog')

        b = Post.get_by_id(int(post_id), parent=blog_key())
        b.delete()
        comments = Comment.all().filter('post_id =', post_id)
        for comment in comments:
            comment.delete()

        self.redirect('/blog/postdeleted')


#
#   Like Post Page for Blog
#
class LikePost(BlogHandler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        b = db.get(key)

        if not b:
            self.error(404)
            return

        user_id = self.user.key().id()
        l = Likes(parent=blog_key(), post_id=int(post_id),
                  user_id=int(user_id))
        l.put()
        self.redirect('/blog/%s' % str(b.key().id()))


#
#   New Blog Post
#
class NewPost(BlogHandler):
    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect("/login")

    def post(self):
        if not self.user:
            self.redirect('/blog')

        subject = self.request.get("subject")
        content = self.request.get("content")
        user_id = self.user.key().id()

        if subject and content:
            b = Post(parent=blog_key(), subject=subject, content=content,
                     user_id=user_id)
            b.put()
            self.redirect('/blog/%s' % str(b.key().id()))
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject=subject, content=content,
                        error=error)


#
#   New Comment
#
class NewComment(BlogHandler):

    def get(self, post_id):
        if self.user:
            self.render("newcomment.html", post_id=post_id)
        else:
            self.redirect("/login")

    def post(self, post_id):
        if not self.user:
            self.redirect('/blog')

        content = self.request.get("content")
        user_id = self.user.key().id()

        if content:
            c = Comment(parent=blog_key(), content=content,
                        post_id=int(post_id), user_id=user_id)
            c.put()
            self.redirect('/blog/%s' % str(post_id))
        else:
            error = "content, please!"
            self.render("newcomment.html", content=content, error=error)


#
#   User class for User object
#
class User(db.Model):
    name = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return cls.get_by_id(uid, parent=users_key())

    @classmethod
    def by_name(cls, name):
        u = cls.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email=None):
        pw_hash = make_pw_hash(name, pw)
        return User(parent=users_key(),
                    name=name,
                    pw_hash=pw_hash,
                    email=email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u


#
#   Blog database model
#
def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


#
#   Post entry
#
class Post(db.Model):
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
    post_id = db.IntegerProperty(required=True)
    user_id = db.IntegerProperty(required=True)


app = webapp2.WSGIApplication(
                              [('/', BlogFront),
                               ('/signup', Register),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/welcome', Welcome),
                               ('/blog/?', BlogFront),
                               ('/blog/newpost', NewPost),
                               ('/blog/([0-9]+)', ShowPost),
                               ('/blog/editpost/([0-9]+)', EditPost),
                               ('/blog/deletepost/([0-9]+)', DeletePost),
                               ('/blog/postdeleted', PostDeleted),
                               ('/blog/likepost/([0-9]+)', LikePost),
                               ('/blog/newcomment/([0-9]+)', NewComment)
                               ], debug=True)
