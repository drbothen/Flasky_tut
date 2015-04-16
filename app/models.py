"""
This module defines our database and table relationships
"""

from app import db  # imports our db (SQLAlchemy) object from our app (__init__)
from hashlib import md5

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Creates a primary key, integer column named ID
    nickname = db.Column(db.String(64), index=True, unique=True)
    """
    Creates a column named nickname with type string that is 64 char in length. index is enabled and all values need to
    be unique
    """
    email = db.Column(db.String(120), index=True, unique=True)
    """
    Creates a column named email with type string that is 120 char in length. index is enabled and all values need to
    be unique
    """
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    """
    db.relationship('many class', backref='field added to many side'
    db.relationship is normally used on the 'one' side of a one to many relationship. With this relationship we
    automatically get a user.posts member that allows us to get all the posts for a given user. The backref field
    defines an object that will be added to the many side that points back at the 'one' side. we can now use post.author
    to get the user instance that created a post
    """
    about_me = db.Column(db.String(140))
    """
    Creates a Column called about_me with type string, length 140
    """
    last_seen = db.Column(db.DateTime)
    """
    Creates a Column called last_seen with type date
    """

    def is_authenticated(self):  # needed by Flask_Login
        return True

    def is_active(self):  # needed by Flask_Login
        return True

    def is_anonymous(self):  # needed by Flask_Login
        return False

    def get_id(self):  # needed by Flask_Login
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/{MD5}?d=mm&s={size}'.format(MD5=md5(self.email.encode('utf-8')).hexdigest(), size=size)

    @staticmethod  # staticmethods are used when a func does not apply to a single instance of the class
    def make_unique_nickname(nickname):  # makes unique nicknames
        if User.query.filter_by(nickname=nickname).first() is None:  # Checks to see if nickname in database
            return nickname  # if not return nickname
        version = 2  # initialize variable
        while True:  # loop to continue running checking nicknames
            new_nickname = nickname + str(version)  # add version variable to nickname
            if User.query.filter_by(nickname=new_nickname).first() is None:  # check database for new nickname
                break  # if not found break away from loop
            version += 1  # if found add 1 to version and repeat above
        return new_nickname  # once a nickname is found to be unique, return nickname

    def __repr__(self):
        return '<User {nickname}>'.format(nickname=self.nickname)
    """
    defines a method for printing this object
    """


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Creates a primary key, integer column named ID
    body = db.Column(db.String(140))  # Creates a column named body with type string, 140 char length
    timestamp = db.Column(db.DateTime)  # Creates a column named timestamp with type datetime
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    """
    Creates a ForeignKey linked to the id column in the user table (provided by the User class)
    """

    def __repr__(self):
        return '<Post {body}>'.format(body=self.body)
    """
    defines a method for printing this object
    """