import os

APP_ROOT = os.path.dirname(os.path.abspath("..run"))


class Config(object):
    CELERY_BROKER_URL = 'redis://localhost:6379/0',
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_DEFAULT_SENDER = "taskqueueapplication@gmail.com"
    MAIL_USERNAME = "taskqueueapplication@gmail.com"
    MAIL_PASSWORD = "firehell8"
    UPLOAD_FOLDER = os.path.join(APP_ROOT, 'app/media')
    ALLOWED_EXTENSIONS = {'mp4', 'webm', 'avi'}
