from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from .forms import LoginForm, EditForm, PostForm
from .models import User, Post
from datetime import datetime
from config import POSTS_PER_PAGE

@app.route('/', methods=['GET', 'POST'])  # get and post required to get submitted data
@app.route('/index', methods=['GET', 'POST'])  # get and post required to get submitted data
@app.route('/index/<int:page>', methods=['GET', 'POST'])  # takes a variable and declares it an interger
@login_required  # Requires a login to view this page
def index(page=1):  # assign a default value to page due to above routes not all provide a value
    form = PostForm()  # create a form object
    if form.validate_on_submit():  # check if form is valid
        post = Post(body=form.post.data, timestamp=datetime.utcnow(), author=g.user)  # create a post object
        db.session.add(post)  # add post object to db session
        db.session.commit()  # commit session to the db
        flash('Your post is now live!')
        return redirect(url_for('index'))  # keeps a refresh action from taking place and cause a dup post object
    # user = g.user  # assigns the user variable to the shared g.user object
    # user = {'nickname': 'JD'} # Fake User  # used during our testing
    posts = g.user.followed_posts().paginate(page, POSTS_PER_PAGE, False)  # pull posts from the database.
    """
    posts = g.user.followed_posts().paginate(page, POSTS_PER_PAGE, False).items keeps only the items from the object
    """
    """
    posts = [ # Fake arrary of posts
              {
                  'author':{'nickname': 'John'},
                  'body': 'Beautiful day in Portland!'
              },
              {
                  'author': {'nickname': 'Susan'},
                  'body': 'The Avengers movie was so cool!'
              },
              {
                  'author': {'nickname': 'Jason'},
                  'body': 'This is so friggin cool!'
              }
    ]
    """
    print Post.query.whoosh_search('post').all()
    return render_template('index.html',
                           title='Home',
                           form=form,
                           posts=posts)


@app.route('/but')
def but():
    return "Hello Stupid!!!"


@app.route('/login', methods=['GET', 'POST'])  # this is our login page. Requires GET and POST to receive data
@oid.loginhandler  # tells flask to user our OpenID handler
def login():
    if g.user is not None and g.user.is_authenticated():  # Checks to see if the user is already logged in
        return redirect(url_for('index'))  # if user is already logged in, redirect to the index page
    form = LoginForm()  # Stores the post request from the LoginForm in form
    if form.validate_on_submit():  # validates the form data
        session['remember_me'] = form.remember_me.data  # Stores the remember me boolean in the session
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])  # Calls the Flask_OpenID login function
    return render_template('login.html',  # Renders the login page/form
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])

# add a check to see if user is currently following following self. if not added self as following
@oid.after_login  # Runs after a login
def after_login(resp):  # this is called after the login attempt. resp variable contains the info returned by the oidp
    if resp.email is None or resp.email == "":  # this is for validation. we require a valid email
        flash('Invalid login. Please try again.')  # display error message on page
        return redirect(url_for('login'))  # redirect back to the login page
    user = User.query.filter_by(email=resp.email).first()  # search our database for the email provided
    if user is None:  # if email is not found. consider this user a new user
        nickname = resp.nickname  # store the nickname value
        if nickname is None or nickname == "":  # if no nickname is provided. create one from the email
            nickname = resp.email.split('@')[0]  # section before the @ will be the users nickname
        nickname = User.make_unique_nickname(nickname)
        user = User(nickname=nickname, email=resp.email)  # Create a new user in database
        db.session.add(user)  # add new user to db session
        db.session.commit()  # commit changes
        db.session.add(user.follow(user))  # user is added to follow themselves
        db.session.commit()  # commit changes
    remember_me = False  # set remember_me value to false incase its not in the session
    if not user.is_following(user):

        """
        checks to insure a user is following themselves. legacy support to implement change for displaying posts
        """

        db.session.add(user.follow(user))
        db.session.commit()
    if 'remember_me' in session:  # load the remember me value from the session
        remember_me =\
        session['remember_me']  # load value
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)  # register the login as valid
    return redirect(request.args.get('next') or url_for('index'))  # return to the page the user asked for or index


@app.route('/logout')  # Route added for user log outs
def logout():
    logout_user()  # Calls the logout_user function to log the user out of the app
    return redirect(url_for('index'))  # Then redirects back to the index page


@app.route('/user/<nickname>')  # <nickname> is an argument
@app.route('/user/<nickname>/<int:page>')
@login_required
def user(nickname, page=1):
    user = User.query.filter_by(nickname=nickname).first()  # Takes the <nickname> argument and performs a database query
    if user is None:  # Checks to See if the nickname actually exists
        flash('User {nickname} not found.'.format(nickname=nickname))  # shows an error if nickname does not exist
        return redirect(url_for('index'))  # redirects to the index page
    posts = user.posts.paginate(page, POSTS_PER_PAGE, False)
    """
    posts = [  # Test Posts
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #1'}
    ]
    """
    return render_template('user.html',  # Renders the user template
                           user=user,  # assigns our user variable to our user for use in our template
                           posts=posts)  # assigns our posts variable for use in our template


@app.route('/edit', methods=['GET', 'POST'])  # edit.html has a form and there for needs methods GET and POST
@login_required  # Requires user to be logged in to view this page
def edit():
    form = EditForm(g.user.nickname)  # form equals our EditForm that we defined in our forms.py
    if form.validate_on_submit():  # validators our form data with the validators attached to the form
        g.user.nickname = form.nickname.data  # g.user.nickname = what was typed into the nickname field
        g.user.about_me = form.about_me.data  # g.user.about_me = what was typed into the about_me field
        db.session.add(g.user)  # add the data entered to the db session
        db.session.commit()  # commit the data to the database
        flash('Your changes have been saved.')  # display message that the changes where saved
        return redirect(url_for('edit'))  # redirect back to the edit page
    else:
        form.nickname.data = g.user.nickname  # load data that is currently in g.user.nickname into nickname field
        form.about_me.data = g.user.about_me  # load data that is currently in g.user.about_me into about_me field
    return render_template('edit.html', form=form)  # render the page using the form EditForm


@app.errorhandler(404)  # error handler for 404 'Not Found' error
def not_found_error(error):  # function for handling 404 errors
    return render_template('404.html'), 404  # Defines the template to use for 404 errors


@app.errorhandler(500)  # error handler for 500 'Internal Server error' error
def internal_error(error):  # function for handling 500 errors
    db.session.rollback()  # roll back database for a working session
    return render_template('500.html'), 500  # Defines the template to use for 500 errors


@lm.user_loader
def load_user(id):  # this function is registered with the lm using the decorator. this will be used to load a user
    return User.query.get(int(id))  # loads user from the database


@app.before_request  # this will cause this function to run before the view func each time a request is received
def before_request():
    g.user = current_user  # this allows all requests to have access to the logged in user. g is shared between requests
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@app.route('/follow/<nickname>')
@login_required
def follow(nickname):
    user = User.query.filter_by(nickname=nickname).first()  # Query database for user
    if user is None:  # checks if a user was returned
        flash('User {nickname} not found.'.format(nickname=nickname))  # error message
        return redirect(url_for('user', nickname=nickname))  # redirect to user page
    if user == g.user:  # check if user is currently logged in user
        flash("You can't follow yourself!")  # error message
        return redirect(url_for('user', nickname=nickname))  # redirect to user page
    u = g.user.follow(user)  # assign user to follow given user
    if u is None:  # check to insure u is not none
        flash('Cannot follow {nickname}.'.format(nickname=nickname))  # error message
        return redirect(url_for('user', nickname=nickname))  # return to user page
    db.session.add(u)  # add object to db session
    db.session.commit()  # commit session
    flash('You are now following {nickname}!'.format(nickname=nickname))  # confirmation message
    return redirect(url_for('user', nickname=nickname))  # return to user page

@app.route('/unfollow/<nickname>')
@login_required
def unfollow(nickname):
    user = User.query.filter_by(nickname=nickname).first()  # query database for user
    if user is None:  # insure user has not be assigned none
        flash('User {nickname} not found'.format(nickname=nickname))  # error message
        return redirect(url_for('index'))  # redirect to user page
    if user == g.user:  # check to insure user does not equal currently logged in user
        flash("You can't unfollow yourself!")  # error message
        return redirect(url_for('user', nickname=nickname))  # return to user page
    u = g.user.unfollow(user)  # execute unfollow func
    if u is None:  # check to insure none was not returned
        flash("You can't unfollow {nickname}.".format(nickname=nickname))  # error message
        return redirect(url_for('user', nickname=nickname))  # return to user page
    db.session.add(u)  # add to db session
    db.session.commit() # commit session
    flash('You have stopped following {nickname}.'.format(nickname=nickname))  # confirmation message
    return redirect(url_for('user', nickname=nickname))  # redirect to user page