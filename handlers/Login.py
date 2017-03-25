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
# Login Handler
#
# Blog project for Udacity Full Stack NanoDegree
# Student:  Candace McCall
# Date:  02/05/2017
#
import os

from handlers import BlogHandler
from models import User
from google.appengine.ext import db


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
