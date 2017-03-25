## Blog application

### Directory structure
    handlers
        __init__.py        Package definition
        BlogFront.py       Front page of blog
        BlogHandler.py     Main Blog Handler
        blogsutil.py       Utility functions used in handlers
        CommentDeleted.py  Comment deleted
        DeleteComment.py   Delete comment
        DeletePost.py      Delete post
        EditComment.py     Edit comment
        EditPost.py        Edit post
        errorcheck.py      Decorator functions used in handlers for error
                           checking
        LikePost.py        Like post
        Login.py           Login
        Logout.py          Logout
        NewComment.py      New comment
        NewPost.py         New post
        PostDeleted.py     Post deleted
        Register.py        Register User
        ShowComment.py     Show comment
        ShowPost.py        Show post
        Signup.py          Signup
        Welcome.py         Welcome
    models
        __init__.py        Package definition
        Comment.py         Comment
        Likes.py           Likes
        Post.py            Post
        User.py            User
    static 
        main.css           Main style sheet
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
     mult-blog-20170206.appspot.com

### To run locally:
     Install Google App Engine SDK
     Download project to your PC.
     Run server:   python dev_appserver.py app.yaml    in the project directory
     Run app at http://localhost:8080




