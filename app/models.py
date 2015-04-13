"""
This module defines our database and table relationships
"""

from app import db  # imports our db (SQLAlchemy) object from our app (__init__)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    """
    db.relationship('manyclass', backref='field added to many side'
    db.relationship is normally used on the 'one' side of a one to many relationship. With this relationship we
    automatically get a user.posts member that allows us to get all the posts for a given user. The backref field
    defines an object that will be added to the many side that points back at the 'one' side. we can now use post.author
    to get the user instance that created a post
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

    def __repr__(self):
        return '<User {nickname}>'.format(nickname=self.nickname)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {body}>'.format(body=self.body)