__author__ = 'jmagady'
from flask_mail import Message
from flask import render_template
from app import mail
from config import ADMINS
from threading import Thread
from app import app


def send_async_email(app, msg):
    with app.app_context():  # (beceause it is a seperate thread) sets up the application context manually because it is threaded (required by flask_mail)
        mail.send(msg)  # sends our message object


def send_email(subject, sender, recipients, text_body, html_body):  # this function sends email
    msg = Message(subject, sender=sender, recipients=recipients)  # creates a message object
    msg.body = text_body  # creates our text version of our email
    msg.html = html_body  # creates our html version of our email
    thr = Thread(target=send_async_email, args=[app, msg])  # Creates a thread
    thr.start()  # starts thread


def follower_notification(followed, follower):  # sets up sending the email
    send_email('[microblog] {follower} is now following you!'.format(follower=follower.nickname),
               ADMINS[0],
               [followed.email],
               render_template('follower_email.txt',
                               user=followed, follower=follower),
               render_template('follower_email.html',
                               user=followed, follower=follower))  # send on follow notficiation to the followee who is now following them
