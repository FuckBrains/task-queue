from app import celery, app, mail
from flask_mail import Message
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from .logger import VideoProgressLogger
import time


@celery.task(bind=True)
def send_async_email(self, email_data):
    msg = Message(subject=email_data['subject'],
                  sender=app.config["MAIL_DEFAULT_SENDER"],
                  recipients=email_data['to'],
                  body=email_data['body'])
    with app.app_context():
        mail.send(msg)

    for i in range(0, 100, 1):
        self.update_state(state="PROGRESS", meta={
                          'current': i, 'total': 100, 'status': 'Sending'})
        time.sleep(0.03)

    return {'current': 100, 'total': 100, 'status': 'Sent to ' + ", ".join(email_data['to'])}



@celery.task(bind=True)
def async_watermark_video(self, filepath):
    clip = VideoFileClip(filepath)
    txt_clip = TextClip(txt="Sample text", fontsize=56,
                        color="white", font="Arial")
    txt_clip.set_position("center")
    txt_clip.set_duration(20)
    video = CompositeVideoClip([clip, txt_clip])
    clip.write_videofile(filepath, logger=VideoProgressLogger(self))
    return {'current': 100, 'total': 100, 'status': "Video processed"}
