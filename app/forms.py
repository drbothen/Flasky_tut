from flask_wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length


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

