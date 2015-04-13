"""
This module defines our database and table relationships
"""

from app import db  # imports our db (SQLAlchemy) object from our app (__init__)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<User {nickname}'.format(nickname=self.nickname)
