from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from app.models import Users

# Forms Here
class LoginForm(FlaskForm):
    username = StringField('Username Or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField("Submit")
    pass

class EntryForm(FlaskForm):
    username = StringField('Username Or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField("Submit")
    pass

class SignupForm(FlaskForm):
    username = StringField('Username Or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_re = PasswordField('Re enter Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please Use a Different Username.')