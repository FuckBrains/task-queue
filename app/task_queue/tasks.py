import os
import time
from .logger import VideoProgressLogger
from app import celery, app, mail
from flask_mail import Message
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import moviepy.video.fx.all as vfx


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
def async_process_video(self, filepath, filename, options):
    # Video
    clip = VideoFileClip(os.path.join(filepath, filename))
    if (options['rotation'] != ''):
        clip = clip.add_mask().rotate(int(options['rotation']))
    if options['duration'] != '' and clip.duration > int(options['duration']):
        clip = clip.set_duration(options['duration'])

    if 'disable-audio' in options.keys():
        if options['disable-audio'] == 'on':
            clip = clip.without_audio()

    if 'black-and-white' in options.keys():
        if options['black-and-white'] == 'on':
            clip = clip.fx(vfx.blackwhite)

    # Text
    txt_clip = TextClip(txt="Test", fontsize=48,
                        color="white", font="Arial")
    # if 'position-x' in options.keys() and 'position-y' in options.keys():
    #     txt_clip = txt_clip.set_position(
    #         options['position-x'], options['position-y'])
    # elif 'position-x' in options.keys():
    #     txt_clip = txt_clip.set_position(options['position-x'], 'top')
    # elif 'position-y' in options.keys():
    #     txt_clip = txt_clip.set_position('left', options['position-y'])

    txt_clip = txt_clip.set_duration(clip.duration)
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
