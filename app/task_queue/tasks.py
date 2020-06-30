from app import celery, app, mail
from flask_mail import Message
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from .logger import VideoProgressLogger
import time
import os


@celery.task(bind=True)
def send_async_email(self, email_data):
    with app.app_context():
        msg = Message(subject=email_data['subject'],
                      recipients=email_data['to'],
                      html=email_data['body']
                      )
        mail.send(msg)

    for i in range(0, 100, 1):
        self.update_state(state="PROGRESS", meta={
                          'current': i, 'total': 100, 'status': 'Sending'})
        time.sleep(0.03)

    return {'current': 100, 'total': 100, 'status': 'Sent to ' + ", ".join(email_data['to'])}


@celery.task(bind=True)
def async_process_video(self, filepath, filename):
    clip = VideoFileClip(os.path.join(filepath, filename))
    txt_clip = TextClip(txt="Sample text", fontsize=56,
                        color="white", font="Arial")
    txt_clip = txt_clip.set_position("center").set_duration(clip.duration)
    video = CompositeVideoClip([clip, txt_clip])
    video.write_videofile(
        os.path.join(filepath, "PROCESSED_" + filename),
        audio_codec='aac',
        temp_audiofile='temp-audio.m4a',
        remove_temp=True,
        logger=VideoProgressLogger(self)
    )
    os.remove(os.path.join(filepath, filename))
    return {'current': 100, 'total': 100, 'status': "Video processed"}
