__author__ = 'jmagady'
from flask_mail import Message
from flask import render_template
from app import mail
from config import ADMINS
from app import app
from .decorators import async


@async  # pulls threading code from decorators
def send_async_email(app, msg):
    with app.app_context():  # (beceause it is a seperate thread) sets up the application context manually because it is threaded (required by flask_mail)
        mail.send(msg)  # sends our message object


def send_email(subject, sender, recipients, text_body, html_body):  # this function sends email
    msg = Message(subject, sender=sender, recipients=recipients)  # creates a message object
    msg.body = text_body  # creates our text version of our email
    msg.html = html_body  # creates our html version of our email
    send_async_email(app, msg)


def follower_notification(followed, follower):  # sets up sending the email
    send_email('[microblog] {follower} is now following you!'.format(follower=follower.nickname),
               ADMINS[0],
               [followed.email],
               render_template('follower_email.txt',
                               user=followed, follower=follower),
               render_template('follower_email.html',
                               user=followed, follower=follower))  # send on follow notficiation to the followee who is now following them
