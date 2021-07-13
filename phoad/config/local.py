import os

import dj_database_url

from utils import merge_dicts
from .common import Common

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Local(Common):
    DEBUG = True

    DATABASES = {
        'default': dj_database_url.config(
            default='postgres://postgres:@postgres:5432/postgres',
            conn_max_age=int(os.getenv('POSTGRES_CONN_MAX_AGE', 600))
        )
    }

    # Testing
    INSTALLED_APPS = Common.INSTALLED_APPS
    SECRET_KEY = 'local'

    # Django Rest Framework
    REST_FRAMEWORK = merge_dicts(Common.REST_FRAMEWORK, {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.TokenAuthentication',
            'rest_framework.authentication.SessionAuthentication',
        )
    })
