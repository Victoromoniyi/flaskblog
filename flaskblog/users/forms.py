from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from flaskblog.models import User

class RegistrationForm(FlaskForm):
     username = StringField('Username', validators=[DataRequired(),
     Length(min=2, max = 25)])
     email = StringField('Email', validators=[DataRequired(), Email()])
     password = PasswordField('Password', validators=[DataRequired()])
     password_confirm = PasswordField('Confirm Password',
     validators=[DataRequired(), EqualTo('password')])
     submit = SubmitField('Sign Up')

     def validate_username(self,username):
         user = User.query.filter_by(username=username.data).first()
         if user:
             raise ValidationError('Username already exists. Please choose another one.')

     def validate_email(self,email):
         user = User.query.filter_by(email=email.data).first()
         if user:
             raise ValidationError('Email already taken. Please use another one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
     username = StringField('Username', validators=[DataRequired(),
     Length(min=2, max = 25)])
     email = StringField('Email', validators=[DataRequired(), Email()])
     picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png','gif'])])
     submit = SubmitField('Update your account')

     def validate_username(self,username):
         if username.data != current_user.username:
             user = User.query.filter_by(username=username.data).first()
             if user:
                 raise ValidationError('Username already exists. Please choose another one.')

     def validate_email(self,email):
         if email.data != current_user.email:
             user = User.query.filter_by(email=email.data).first()
             if user:
                 raise ValidationError('Email already taken. Please use another one.')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. Please register.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password',
    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
