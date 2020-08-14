import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '1l0v3t4c0$'
    VCAP_APPLICATION = os.environ.get('VCAP_APPLICATION')