from __future__ import absolute_import, unicode_literals

from .base import *

DEBUG = True
HTML_MINIFY = True

SECRET_KEY = '1do7a%$r^^*e3%44@21gt9$j27bsg$^^=vtvmpc@ul-9bbt%bo'

SETTINGS_DIR = os.path.dirname(__file__)
PROJECT_PATH = os.path.abspath(os.path.join(SETTINGS_DIR, os.pardir))
DATABASE_PATH = os.path.abspath(os.path.join(PROJECT_PATH,
                                             'schaermu_ch.db'))
DB_ENV = os.environ.get('TEST_DB')
if DB_ENV == 'sqlite':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': DATABASE_PATH,
        }
    }

try:
    from .local import *
except ImportError:
    pass
