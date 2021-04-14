from hashlib import md5
import os
from flask import current_app, render_template, request
from PIL import Image
from flask_mail import Message
from decouple import config
from travel_planner import mail


def save_picture(form_picture, user_email):
    random_hex = md5(user_email.encode('utf-8')).hexdigest()
    __, ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + ext
    picture_path = os.path.join(
        current_app.root_path, 'static/profile_pics', picture_fn)

    size = (128, 128)
    i = Image.open(form_picture)
    i.thumbnail(size)
    i.save(picture_path)
    return picture_fn


def send_reset_request(user):
    token = user.get_token()
    msg = Message()
    msg.recipients = [user.email]
    msg.subject = 'Password Reset Request'
    msg.sender = config('MAIL_USERNAME')
    msg.html = render_template('reset_email.html', token=token)
    mail.send(msg)
