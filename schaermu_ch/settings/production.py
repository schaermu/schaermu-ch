from __future__ import absolute_import, unicode_literals

import dj_database_url

from .base import *

import os

env = os.environ.copy()
SECRET_KEY = env.get('SECRET_KEY')

DEBUG = False

try:
    from .local import *
except ImportError:
    pass

ANYMAIL = {
    "MAILGUN_API_KEY": env['MAILGUN_API_KEY']
}
EMAIL_BACKEND = "anymail.backends.mailgun.MailgunBackend"
DEFAULT_FROM_EMAIL = "noreply@schaermu.ch"

GA_KEY_CONTENT = env['GOOGLE_SERVICE_PRIVATE_KEY']

SECURE_SSL_REDIRECT = True

# Parse database configuration from $DATABASE_URL
DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

COMPRESS_OFFLINE = True
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_CSS_HASHING_METHOD = 'content'
