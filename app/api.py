from flask import request, render_template
from werkzeug.utils import secure_filename
from flask_uploads import IMAGES

from app.util import allowed_file, upload_file_to_s3

from app import app


@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    if request.method == 'POST':
        try:
            file = request.files["img_input"]
            if file.filename == "":
                errors.append('No file provided')
            elif file:
                if not allowed_file(file.filename):
                    errors.append('File type not allowed. Only image files with the following extensions are accepted:'
                                  ' %s' % str(IMAGES))
                else:
                    file.filename = secure_filename(file.filename)
                    output = upload_file_to_s3(file, app.config["S3_BUCKET_NAME"])
                    return render_template('img.html', image=output)
        except Exception as e:
            errors.append(str(e) + ' Possible reasons: No file provided, Invalid file type, File not found.')
    return render_template('index.html', errors=errors)
