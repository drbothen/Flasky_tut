__author__ = 'jmagady'

import os
import unittest

from config import basedir
from app import app, db
from app.models import User


class TestCase(unittest.TestCase):  # holds all of our tests
    def setUp(self):  # special method ran before tests
        app.config['TESTING'] = True  # configures app for TESTING
        app.config['WTF_CSRF_ENABLED'] = False  # sets WTF_CSRF_ENABLED to false
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db') # sets location of tmp db
        self.app = app.test_client()  # sets up test client
        db.create_all()  # creates the tmp database

    def tearDown(self):  # Special method ran after tests
        db.session.remove()  # removes the session
        db.drop_all()  # drops the database

    def test_avatar(self):  # tests the avatar func
        u = User(nickname='john', email='john@example.com')  # creates a user
        avatar = u.avatar(128)  # calls the avatar attribute
        expected = 'http://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6'  # sets expected return value
        assert avatar[0:len(expected)] == expected  # checks to see if returned value matches expected

    def test_make_unique_nickname(self):  # Checks our unique nickname algorithm
        u = User(nickname='john', email='john@example.com')  # creates a user
        db.session.add(u)  # adds the new user to the db session
        db.session.commit()  # commits the user to the database
        nickname = User.make_unique_nickname('john')  # runs our unique nickname function
        assert nickname != 'john'  # checks to see if the nickname is not john
        u = User(nickname=nickname, email='susan@example.com')  # creates a 2nd user
        db.session.add(u)  # adds user to the db session
        db.session.commit()  # commits the new user to the database
        nickname2 = User.make_unique_nickname('john')  # runs the unique_nickname function
        assert nickname2 != 'john'  # checks to makes sure new nickname does not equal existing
        assert nickname2 != nickname  # check to make sure new nickname does not equal existing

if __name__ == '__main__':
    unittest.main()
