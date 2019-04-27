import os

SECRET_KEY = 'super-secret'
PYCHARM_DEBUG = True
CWD = os.getcwd()
UPLOADS_DEFAULT_DEST = os.path.join(CWD, 'instance')
UPLOADS_SRC = os.path.join(CWD, 'src/instance')
IMAGES_FOLDER = UPLOADS_DEFAULT_DEST + '/images'
IMAGES_SRC = UPLOADS_SRC + '/images'
TEST_IMAGES_FOLDER = 'images'
TEST_IMAGES_INVALID_FOLDER = 'images_invalid'
