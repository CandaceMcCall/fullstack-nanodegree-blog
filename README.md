## Blog application

### Directory structure
    static 
        main.css    Main style sheet
    templates
        base.html          Base html file for other template files.  Contains
                           links for signup, login, logout, blog main page
        comment.html       Comment html for viewing
        deletepost.html    Confirmation page that views post to be deleted
        editpost.html      Form for editing post with confirmation to update
        front.html         Main front page of blog
        login.html         Login form
        newcomment.html    Comment form
        permalink.html     Viewing page for post
        post.html          Post html for viewing
        postdeleted.html   Page indicating post deletion successful
        signup.html        Signup form
        welcome.html       Welcome page displayed when user signs up

     main.py               Main program
     

### Links on web site
     /                          Blog Front Page
     /blog                      Blog Front Page
     /signup                    Sign Up
     /login                     Login
     /logout                    Logout
     /welcome                   Welcome
     /blog/newpost              Mew Post
     /blog/([0-9]+)             Show Post
     /blog/editpost([0-9]+)     Edit Post
     /blog/deletepost([0-9]+)   Delete Post
     /blog/postdeleted          Post Deleted
     /blog/likepost([0-9]+)     Like Post
     /blog/newcomment([0-9]+)   Comment on Post


### To run type in browser:
	python udacity-blog-project-157905.appspot.com

### To run application server, type:
	python application.py

### Run application in browser by the following address:   
    http://localhost:8000


