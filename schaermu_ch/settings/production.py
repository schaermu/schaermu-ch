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

SECURE_SSL_REDIRECT = True

# Parse database configuration from $DATABASE_URL
DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

AWS_REGION = 'eu-central-1'
AWS_ACCESS_KEY_ID = env['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = env['AWS_SECRET_ACCESS_KEY']
AWS_S3_BUCKET_NAME = env['S3_BUCKET']
AWS_S3_BUCKET_AUTH = False

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
DEFAULT_FILE_STORAGE = 'schaermu_ch.s3utils.StaticRootS3BotoStorage'

S3_URL = "https://s3.{0}.amazonaws.com/{1}".format(AWS_REGION,
                                                   AWS_S3_BUCKET_NAME)
MEDIA_URL = S3_URL + '/media/'

COMPRESS_OFFLINE = True
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_CSS_HASHING_METHOD = 'content'
