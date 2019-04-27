import os

import pytest
from flask import request
from werkzeug.datastructures import FileStorage

from app import app
from util import IMAGE_SET, clean_images_dir


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
            rv = c.post('/', data=dict(upload=img_file), follow_redirects=True)

            assert (request.url + 'img/' + img).encode('utf-8') in rv.data, 'Image URL should be found in response body'
            assert img in os.listdir(app.config['IMAGES_FOLDER']), 'Image should be saved in instance dir'

            rv = c.get('/img/' + img)

            assert rv.status_code == 200, 'Should be able to get image after upload'
            assert 'image' in rv.content_type, 'Content type should be of image type'
            assert img.split('.')[-1] in IMAGE_SET.extensions, 'File ext should be valid image type'


def test_upload_image_fail(setup):
    """Test uploads of invalid images"""
    with app.test_client() as c:
        for img in os.listdir(app.config['TEST_IMAGES_INVALID_FOLDER']):
            img_file = FileStorage(filename=img)
            rv = c.post('/', data=dict(upload=img_file), follow_redirects=True)

            assert b'ERROR' in rv.data and b'Only image files allowed' in rv.data, 'Invalid image uploads should' \
                                                                                   ' display error'
            assert img not in os.listdir(app.config['IMAGES_FOLDER']), 'Invalid image uploads should not be saved' \
                                                                           ' in instance dir'

            rv = c.get('/img/' + img)

            assert rv.status_code == 404, 'Should not be able to get invalid image, because it should have never' \
                                          ' been saved in the first place'
            assert img.split('.')[-1] not in IMAGE_SET.extensions, 'File ext should be invalid image type'

        rv = c.post('/', follow_redirects=True)
        assert b'ERROR' in rv.data and b'No file provided' in rv.data, 'Empty file uploads should display error'


def test_cleanup(setup):
    """Test cleanup of images instance directory"""
    test_clean_func = clean_images_dir(sum)
    test_clean_func([])
    assert len(os.listdir(app.config['IMAGES_FOLDER'])) == 0, 'Instance dir should be empty after cleanup call'

    with app.test_client() as c:
        for img in os.listdir(app.config['TEST_IMAGES_FOLDER']):
            img_file = FileStorage(filename=img)
            c.post('/', data=dict(upload=img_file), follow_redirects=True)

            assert img in os.listdir(app.config['IMAGES_FOLDER']), 'Instance dir should contain uploaded image'

            c.get('/')

            assert img not in os.listdir(app.config['IMAGES_FOLDER']), 'Image should not be found after GET request,' \
                                                                       ' because it is wrapped in cleanup func'
            assert len(os.listdir(app.config['IMAGES_FOLDER'])) == 0, 'Instance dir should be empty after cleanup' \
                                                                      ' call from GET request'
