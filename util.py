from functools import wraps

from flask_uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField

import os


IMAGE_SET = UploadSet('images', IMAGES)


class ImageForm(FlaskForm):
    upload = FileField('image', validators=[
        FileRequired('No file provided.'),
        FileAllowed(IMAGE_SET, 'Only image files allowed.')
    ])
    submit = SubmitField('Submit')


def clean_dir_helper(path):
    for url in os.listdir(path):
        img = os.path.join(path, url)
        try:
            if os.path.isfile(img):
                os.unlink(img)
        except Exception as e:
            print(e)


def clean_images_dir(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from app import app
        instance_path = app.config['IMAGES_FOLDER']
        if os.path.isdir(instance_path):
            clean_dir_helper(instance_path)
        src_instance_path = app.config['IMAGES_SRC']
        if os.path.isdir(src_instance_path):
            clean_dir_helper(src_instance_path)
        return f(*args, **kwargs)
    return decorated_function
