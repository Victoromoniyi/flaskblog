import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail

def save_picture(form_picture):
    random_hex = secrets.token_hex(7)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pictures', picture_fn)
    size_output = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(size_output)
    i.save(picture_path)
    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
    sender='noreply@flaskblog.com',
    recipients=[user.email])

    msg.body = f'''To reset your password, please visit the following link:
{url_for('utils.reset_token', token=token, _external=True)}

If you did not request this password being sent, then ignore this email. If
you think you did not receive an email, please check your spam folder.
'''
    mail.send(msg)
