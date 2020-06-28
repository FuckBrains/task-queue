from flask import render_template, request, url_for, jsonify
from .. import app, limiter
from .tasks import send_async_email
import uuid


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/status/<task_id>")
def task_status(task_id):
    process = send_async_email.AsyncResult(task_id)
    if process.state == 'PENDING':
        response = {
            'id': task_id,
            'state': process.state,
            'current': 0,
            'total': 1,
            'status': "Pending"
        }
    elif process.state != 'FAILURE':
        response = {
            'id': task_id,
            'state': process.state,
            'current': process.info.get('current', 0),
            'total': process.info.get('total', 1),
            'status': process.info.get('status', '')
        }
    else:
        response = {
            'id': task_id,
            'state': process.state,
            'current': 1,
            'total': 1,
            'status': str(process.info)
        }
    return jsonify(response)


@app.route("/tasks/send-email")
def send_email_get():
    return render_template("send_email.html")


@app.route("/tasks/send-email", methods=["POST"])
@limiter.limit("10 per hour")
def send_email():
    email = request.form.getlist("email[]")
    message = request.form["message"]
    email_data = {
        'subject': "Sample message from localhost",
        'to': email,
        'body': f"""
        This is a test email sent from a bachground Celery task.
         Message from anonymous user:
         "{message}"
         If there is some problems, please contact with developer.
         """
    }
    if request.form['submit'] == "Send":
        task = send_async_email.apply_async(
            args=[email_data], task_id=uuid.uuid4().hex)
    else:
        task = send_async_email.apply_async(args=[email_data], countdown=60)
    return jsonify({"location": url_for('task_status', task_id=task.id)}), 202


@app.route("/tasks/watermark-video", methods=["GET", "POST"])
def watermark_video():
    if request.method == "GET":
        return render_template("video_watermark.html")
    if 'file' not in request.files:
        return jsonify({'error': "No file part"}), 204

    file = request.files["file"]
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 204
    if file and 
