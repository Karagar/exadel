import os


class AWS_SETTINGS:
    REGION = os.getenv('REGION')
    ACCESS_KEY = os.getenv('ACCESS_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')
    BUCKET = os.getenv('BUCKET')
