from flask import Flask
from celery import Celery
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .config import Config
import os


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)
celery = make_celery(app)
limiter = Limiter(app=app, key_func=get_remote_address)

from . import task_queue
