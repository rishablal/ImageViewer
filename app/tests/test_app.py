import os
import pytest

from flask_uploads import IMAGES
from werkzeug.datastructures import FileStorage

from app import app


@pytest.fixture
def setup():
    """Setup testing config"""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    yield app


def test_upload_image(setup):
    """Successful uploads of images"""
    with app.test_client() as c:
        for img in os.listdir(app.config['TEST_IMAGES_FOLDER']):
            img_file = FileStorage(filename=img)
            rv = c.post('/', data=dict(img_input=img_file), follow_redirects=True)

            assert rv.status_code == 200, 'Should get 200 response for successful upload'
            assert (app.config['S3_LOCATION'] + img).encode('utf-8') in rv.data, 'Image URL should be found in' \
                                                                                 ' response body'
            assert img.split('.')[-1] in IMAGES, 'File ext should be valid image type'


def test_upload_image_fail(setup):
    """Test uploads of invalid images"""
    with app.test_client() as c:
        for img in os.listdir(app.config['TEST_IMAGES_INVALID_FOLDER']):
            img_file = FileStorage(filename=img)
            rv = c.post('/', data=dict(img_input=img_file), follow_redirects=True)

            assert b'ERROR' in rv.data and b'File type not allowed' in rv.data, 'Invalid image uploads should' \
                                                                                ' display error'
            assert img.split('.')[-1] not in IMAGES, 'File ext should be invalid image type'

        rv = c.post('/', follow_redirects=True)
        assert b'ERROR' in rv.data and b'No file provided' in rv.data, 'Empty file uploads should display error'
