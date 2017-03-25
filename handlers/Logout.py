#!/usr/bin/env python
#
# Logout Handler
#
# Blog project for Udacity Full Stack NanoDegree
# Student:  Candace McCall
# Date:  02/05/2017
#


from handlers import BlogHandler


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
