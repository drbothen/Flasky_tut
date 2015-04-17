__author__ = 'jmagady'

import os
import unittest
from datetime import datetime, timedelta
from config import basedir
from app import app, db
from app.models import User, Post


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

    def test_follow(self):
        u1 = User(nickname='john', email='john@example.com')  # Create user 1
        u2 = User(nickname='susan', email='susan@example.com')  # Create user 2
        db.session.add(u1)  # add user 1 to the session
        db.session.add(u2)  # add user 2 to the session
        db.session.commit()  # commit the session
        assert u1.unfollow(u2) is None  # unfollow should return none
        u = u1.follow(u2)  # set user 1 to following user 2
        db.session.add(u)  # add to db session
        db.session.commit()  # commit the session
        assert u1.follow(u2) is None  # checks to make sure it wont add a user twice
        assert u1.is_following(u2)  # test is_following
        assert u1.followed.count() == 1  # should only allow user to be followed once
        assert u1.followed.first().nickname == 'susan'  # insures john is following susan
        assert u2.followers.count() == 1  # should only allow user to be followed once
        assert u2.followers.first().nickname == 'john'  # insures susan is following john
        u = u1.unfollow(u2)  # set john to unfollow susan
        assert u is not None  # insure it does not return None
        db.session.add(u)  # add to session
        db.session.commit()  # commit session to database
        assert not u1.is_following(u2)  # check to insure john is not following susan
        assert u1.followed.count() == 0  # check to insure john is not following anyone
        assert u2.followers.count() == 0  # check to insure susan has no followers

    def test_follow_posts(self):
        # make four users
        u1 = User(nickname='john', email='john@example.com')
        u2 = User(nickname='susan', email='susan@example.com')
        u3 = User(nickname='mary', email='mary@example.com')
        u4 = User(nickname='david', email='david@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.add(u4)
        # make four posts
        utcnow = datetime.utcnow()
        p1 = Post(body="post from john", author=u1, timestamp=utcnow + timedelta(seconds=1))
        p2 = Post(body="post from susan", author=u2, timestamp=utcnow + timedelta(seconds=2))
        p3 = Post(body="post from mary", author=u3, timestamp=utcnow + timedelta(seconds=3))
        p4 = Post(body="post from david", author=u4, timestamp=utcnow + timedelta(seconds=4))
        db.session.add(p1)
        db.session.add(p2)
        db.session.add(p3)
        db.session.add(p4)
        db.session.commit()
        # setup the followers
        u1.follow(u1)  # john follows himself
        u1.follow(u2)  # john follows susan
        u1.follow(u4)  # john follows david
        u2.follow(u2)  # susan follows herself
        u2.follow(u3)  # susan follows mary
        u3.follow(u3)  # mary follows herself
        u3.follow(u4)  # mary follows david
        u4.follow(u4)  # david follows himself
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.add(u4)
        db.session.commit()
        # check the followed posts of each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        assert len(f1) == 3
        assert len(f2) == 2
        assert len(f3) == 2
        assert len(f4) == 1
        assert f1 == [p4, p2, p1]
        assert f2 == [p3, p2]
        assert f3 == [p4, p3]
        assert f4 == [p4]

if __name__ == '__main__':
    unittest.main()
