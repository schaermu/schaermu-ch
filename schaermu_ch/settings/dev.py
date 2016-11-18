from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1do7a%$r^^*e3%44@21gt9$j27bsg$^^=vtvmpc@ul-9bbt%bo'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

GA_KEY_FILEPATH = '.google-analytics_sa_key.json'

try:
    from .local import *
except ImportError:
    pass
