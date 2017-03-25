#!/usr/bin/env python
#
# PostDeleted BlogHandler
#
# Blog project for Udacity Full Stack NanoDegree
# Student:  Candace McCall
# Date:  02/05/2017
#


from handlers import BlogHandler


#
#    Post Deleted Class
#
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
