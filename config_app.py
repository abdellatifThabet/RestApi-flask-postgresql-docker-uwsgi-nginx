import logging
import os


class ConfigApp(object):
    # generic
    DEBUG = os.environ.get('DEBUG', False)
    TESTING = os.environ.get('TESTING', False)
    LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', logging.NOTSET)

    # security
    CSRF_ENABLED = os.environ.get('CSRF_ENABLED', False)
    SECRET_KEY = os.environ['SECRET_KEY']

    # swagger
    SWAGGER_UI_DOC_EXPANSION = 'list'

    # sqlalchemy
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = ConfigApp()
