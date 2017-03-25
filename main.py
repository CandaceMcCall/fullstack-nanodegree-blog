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
import webapp2

from handlers import BlogFront, Register, Login, Logout, Welcome, BlogFront
from handlers import NewPost, ShowPost, EditPost, DeletePost, PostDeleted
from handlers import LikePost, ShowComment, NewComment, EditComment
from handlers import DeleteComment
from handlers import CommentDeleted


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
