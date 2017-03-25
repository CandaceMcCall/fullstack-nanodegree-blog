#!/usr/bin/env python
#
# Register Handler
#
# Blog project for Udacity Full Stack NanoDegree
# Student:  Candace McCall
# Date:  02/05/2017
#


from handlers import Signup
from models import User


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
