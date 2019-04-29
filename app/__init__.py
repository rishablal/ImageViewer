import os

from flask import Flask
from flask_cors import CORS

import boto3

# Setup app
app = Flask(__name__, instance_relative_config='')
app.config.from_pyfile('config.py', silent=True)
app.config.SECRET_KEY = os.urandom(24)

# Setup CORS
CORS(app)

# Setup S3
s3 = boto3.client(
   "s3",
   aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
   aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY']
)

# import endpoints
from app import api
