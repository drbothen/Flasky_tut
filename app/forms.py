from flask_wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length
from app.models import User


class LoginForm(Form):  # this class details the form fields for the login template
    openid = StringField('openid', validators=[DataRequired()])
    """
    designates this field as a string field. names openid. the validators argument specifies that Data is required
    and will not be submitted without it
    """
    remember_me = BooleanField('remember_me', default=False)
    """
    designates this field as a Boolean field. sets the name of the field and the default argument, defaults this setting
    to False
    """


class EditForm(Form):  # this class details the form used for editing user profiles
    nickname = StringField('nickname', validators=[DataRequired()])  # this field allows users to change their nickname
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])
    """
    this field allows users to add information about themselves
    """

    def __init__(self, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):  # validate is called automatically
        if not Form.validate(self):  # required for validation (need more info)
            return False
        if self.nickname.data == self.original_nickname:  # Checks to see if the new nickname equals the old nickname
            return True  # if it does return true
        user = User.query.filter_by(nickname=self.nickname.data).first()  # check the database for the new nickname
        if user is not None:  # checks to see if anything was returned from the database
            self.nickname.errors.append('This nickname is already in use. Please choose another one')
            """
            Sets the error data for the duplicate nickname
            """
            return False
        return True


class PostForm(Form):  # form for posts
    post = StringField('post', validators=[DataRequired()])  # designates a string field that requires data


class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])


