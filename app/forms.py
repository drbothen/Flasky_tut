from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


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