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

from models import User, Post, Comment, Likes
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
#   Blog key
#
def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


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


#
#   Login class
#
class Login(BlogHandler):
    """
    Login:   Handler for Login
    Args:
            BlogHandler:     Blog Handler
    """
    def get(self):
        """
        get:   Get
        Args:
                self:   This object
        """
        self.render("login.html")

    def post(self):
        """
        post:   Post
        Args:
                self:   This object
        """
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
    """
    Logout:   Handler for Logout
    Args:
            BlogHandler:     Blog Handler
    """
    def get(self):
        """
        get:   Get
        Args:
                self:   This object
        """
        self.logout()
        self.redirect('/signup')


#
#    Register class
#
class Register(Signup):
    """
    Register:   Handler for Registering New User
    Args:
            Signup:     Signup Handler
    """
    def done(self):
        """
        done:   Done
        Args:
                self:   This object
        """
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
    """
    Welcome:   Handler for Welcome
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
            self.render('welcome.html', username=self.user.name)
        else:
            self.redirect('/signup')


#
#    Post Deleted Class

class PostDeleted(BlogHandler):
    """
    PostDeleted:   Post Deleted Class
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
            self.render('postdeleted.html')
        else:
            self.redirect('/login')


#
#   Blog Front Page for Blog
#
class BlogFront(BlogHandler):
    """
    BlogFront:   Blog Front Page
    Args:
            BlogHandler:     Blog Handler
    """
    def get(self):
        """
        get:   Get
        Args:
                self:   This object
        """
        entries = Post.all().order('-created')
        self.render("front.html", posts=entries)


#
#   Show Post Class for Blog
#
class ShowPost(BlogHandler):
    """
    ShowPost:   Show Post
    Args:
            BlogHandler:     Blog Handler
    """
    def get(self, post_id):
        """
        get:   Get
        Args:
                self:   This object
        """
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.render('notfound.html')
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
    """
    EditPost:   Edit Post
    Args:
            BlogHandler:     Blog Handler
    """
    def get(self, post_id):
        """
        get:   Get
        Args:
                self:   This object
        """
        b = Post.get_by_id(int(post_id), parent=blog_key())

        if not b:
            self.render('notfound.html')
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
        """
        post:   Post
        Args:
                self:   This object
                post_id:    Post ID
        """
        if not self.user:
            return self.redirect('/login')

        b = Post.get_by_id(int(post_id), parent=blog_key())
#
#       Check that user IDs match
#
        user_id = self.user.key().id()
        if b.user_id != user_id:
            return self.redirect('/blog/%s' % str(b.key().id()))

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
    """
    DeletePost:   Delete Post
    Args:
            BlogHandler:     Blog Handler
    """
    def get(self, post_id):
        """
        get:   Get
        Args:
                self:   This object
                post_id:    Post ID
        """
        b = Post.get_by_id(int(post_id), parent=blog_key())

        if not b:
            self.render('notfound.html')
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
        """
        post:   Post
        Args:
                self:   This object
                post_id:    Post ID
        """
        if not self.user:
            return self.redirect('/login')

        b = Post.get_by_id(int(post_id), parent=blog_key())
#
#       Check that user IDs match
#
        user_id = self.user.key().id()
        if b.user_id != user_id:
            return self.redirect('/blog/%s' % str(b.key().id()))
        b.delete()
        comments = Comment.all().filter('post_id =', post_id)
        for comment in comments:
            comment.delete()

        self.redirect('/blog/postdeleted')


#
#   Like Post Page for Blog
#
class LikePost(BlogHandler):
    """
    LikePost:   Like Post
    Args:
            BlogHandler:     Blog Handler
    """
    def get(self, post_id):
        """
        get:   Get
        Args:
                self:   This object
                post_id:    Post ID
        """
        if not self.user:
            return self.redirect('/login')

        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        b = db.get(key)

        if not b:
            self.render('notfound.html')
            return
#
#       Check that user IDs do not match
#
        user_id = self.user.key().id()
        if b.user_id == user_id:
            self.redirect('/blog/%s' % str(b.key().id()))

        if b.is_liked_by_user(user_id) == 'Liked':
            self.redirect('/blog/%s' % str(b.key().id()))

        l = Likes(parent=blog_key(), post_id=int(post_id),
                  user_id=int(user_id))
        l.put()
        self.redirect('/blog/%s' % str(b.key().id()))


#
#   New Blog Post
#
class NewPost(BlogHandler):
    """
    NewPost:   New Post
    Args:
            BlogHandler:     Blog Handler
    """
    def get(self):
        """
        get:   Get
        Args:
                self:   This object
                post_id:    Post ID
        """
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect("/login")

    def post(self):
        """
        post:   Post
        Args:
                self:   This object
        """
        if not self.user:
            return self.redirect('/login')

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
#   Show Comment Class for Blog
#
class ShowComment(BlogHandler):
    """
    ShowPost:   Show Comment
    Args:
            BlogHandler:     Blog Handler
    """
    def get(self, comment_id):
        """
        get:   Get
        Args:
                self:   This object
        """
        key = db.Key.from_path('Comment', int(comment_id), parent=blog_key())
        comment = db.get(key)

        if not comment:
            self.render('notfound.html')
            return

        self.render('showcomment.html', comment=comment)


#
#   New Comment
#
class NewComment(BlogHandler):
    """
    NewComment:   New Comment
    Args:
            BlogHandler:     Blog Handler
    """
    def get(self, post_id):
        """
        get:   Get
        Args:
                self:   This object
                post_id:    Post ID
        """
        if self.user:
            self.render("newcomment.html", post_id=post_id)
        else:
            self.redirect("/login")

    def post(self, post_id):
        """
        post:   Post
        Args:
                self:   This object
                post_id:    Post ID
        """
        if not self.user:
            return self.redirect('/login')

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
#   Edit Comment Page for Blog
#
class EditComment (BlogHandler):
    """
    EditComment:   New Comment
    Args:
            BlogHandler:     Blog Handler
    """
    def get(self, comment_id):
        """
        get:   Get
        Args:
                self:   This object
                comment_id:    Comment ID
        """
        c = Comment.get_by_id(int(comment_id), parent=blog_key())

        if not c:
            self.render('notfound.html')
            return
#
#       Check that user IDs match
#
        user_id = self.user.key().id()
        if c.user_id != user_id:
            self.redirect('/blog/%s' % str(c.key().id()))

        content = c.content
        self.render('editcomment.html', content=content,
                    comment_id=comment_id)

    def post(self, comment_id):
        """
        post:   Post
        Args:
                self:   This object
                comment_id:    Comment ID
        """
        if not self.user:
            return self.redirect('/login')

        c = Comment.get_by_id(int(comment_id), parent=blog_key())
        content = self.request.get("content")

        if content:
            c.content = content
            c.put()
            self.redirect('/blog/comment/%s' % str(c.key().id()))
        else:
            error = "content, please!"
            self.render("editcomment.html", content=content,
                        error=error)


#
#   Delete Comment Page for Blog
#
class DeleteComment(BlogHandler):
    """
    DeleteComment:   Delete Comment
    Args:
            BlogHandler:     Blog Handler
    """
    def get(self, comment_id):
        """
        get:   Get
        Args:
                self:   This object
                comment_id:    Comment ID
        """
        c = Comment.get_by_id(int(comment_id), parent=blog_key())

        if not c:
            self.render('notfound.html')
            return
#
#       Check that user IDs match
#
        user_id = self.user.key().id()
        if c.user_id != user_id:
            self.redirect('/blog/comment/%s' % str(c.key().id()))

        content = c.content
        self.render('deletecomment.html', content=content,
                    comment_id=comment_id)

    def post(self, comment_id):
        """
        post:   Post
        Args:
                self:   This object
                comment_id:    Comment ID
        """
        if not self.user:
            return self.redirect('/login')

        c = Comment.get_by_id(int(comment_id), parent=blog_key())
#
#       Check that user IDs match
#
        user_id = self.user.key().id()
        if c.user_id != user_id:
            return self.redirect('/blog/comment/%s' % str(c.key().id()))
        c.delete()
        comments = Comment.all().filter('comment_id =', comment_id)
        for comment in comments:
            comment.delete()

        self.redirect('/blog/commentdeleted')


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
                               ('/blog/comment/([0-9]+)', ShowComment),
                               ('/blog/newcomment/([0-9]+)', NewComment),
                               ('/blog/editcomment/([0-9]+)', EditComment),
                               ('/blog/deletecomment/([0-9]+)', DeleteComment),
                               ('/blog/commentdeleted', CommentDeleted),
                               ], debug=True)
