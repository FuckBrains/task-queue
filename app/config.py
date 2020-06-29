import os

APP_ROOT = os.path.dirname(os.path.abspath("..run"))


class Config(object):
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = 'taskqueueapplication@gmail.com'
    UPLOAD_FOLDER = os.path.join(APP_ROOT, 'app/media')
    ALLOWED_EXTENSIONS = {'mp4', 'webm', 'avi'}
