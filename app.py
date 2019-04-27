import os

import express
from flask import Flask, request, redirect, url_for, render_template, flash, send_from_directory
from flask_cors import CORS
from flask_uploads import configure_uploads
from werkzeug.utils import secure_filename

from util import clean_images_dir, IMAGE_SET, ImageForm

app = Flask(__name__, static_url_path='')
app.config.from_pyfile('config.py', silent=True)
app.config.SECRET_KEY = os.urandom(24)
configure_uploads(app, (IMAGE_SET,))

# Setup CORS
CORS(app)


@app.route('/', methods=['GET', 'POST'])
@clean_images_dir
def index():
    form = ImageForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            f = form.upload.data
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['IMAGES_FOLDER'], filename))
            return render_template('img.html', image=filename, url=request.url)
    return render_template('index.html', form=form)


@app.route('/img/<image>', methods=['GET'])
def get_image(image):
    return send_from_directory(app.config['IMAGES_FOLDER'], image)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
