from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from .forms import LoginForm
from .models import User

@app.route('/')
@app.route('/index')
@login_required  # Requires a login to view this page
def index():
    user = g.user  # assigns the user variable to the shared g.user object
    # user = {'nickname': 'JD'} # Fake User  # used during our testing
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
    return render_template('index.html',
                           title='Home',
                           user=user,
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
        user = User(nickname=nickname, email=resp.email)  # Create a new user in database
        db.session.add(user)  # add new user to db session
        db.session.commit()  # commit changes
    remember_me = False  # set remember_me value to false incase its not in the session
    if 'remember_me' in session:  # load the remember me value from the session
        remember_me = session['remember_me']  # load value
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)  # register the login as valid
    return redirect(request.args.get('next') or url_for('index'))  # return to the page the user asked for or index


@lm.user_loader
def load_user(id):  # this function is registered with the lm using the decorator. this will be used to load a user
    return User.query.get(int(id))  # loads user from the database


@app.before_request  # this will cause this function to run before the view func each time a request is received
def before_request():
    g.user = current_user  # this allows all requests to have access to the logged in user. g is shared between requests