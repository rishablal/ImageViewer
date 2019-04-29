import os

SECRET_KEY = 'super-secret'
PYCHARM_DEBUG = True
CWD = os.getcwd()
TEST_IMAGES_FOLDER = os.path.join(CWD, 'images')
TEST_IMAGES_INVALID_FOLDER = os.path.join(CWD, 'images_invalid')

S3_BUCKET_NAME = 'acmeimages'
S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET_NAME)
