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
# Welcome BlogHandler
#
# Blog project for Udacity Full Stack NanoDegree
# Student:  Candace McCall
# Date:  02/05/2017
#


from handlers import BlogHandler


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
