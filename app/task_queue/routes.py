from flask import render_template, request, url_for, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import uuid
import os
from .tasks import send_async_email, async_process_video
from .. import app, limiter


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower(
           ) in app.config["ALLOWED_EXTENSIONS"]


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
            'total': 100,
            'status': "Pending",
            'result': None
        }
    elif process.state == 'SUCCESS':
        response = {
            "id": task_id,
            'state': process.state,
            'current': 100,
            'total': 100,
            'status': process.info.get('status', ''),
            'result': request.args.get("result")}
    elif process.state != 'FAILURE':
        response = {
            'id': task_id,
            'state': process.state,
            'current': process.info.get('current', 0),
            'total': process.info.get('total', 100),
            'status': process.info.get('status', ''),
            'result': None
        }
    else:
        response = {
            'id': task_id,
            'state': process.state,
            'current': 0,
            'total': 100,
            'status': "ERROR:" + str(process.info),
            'result': None
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
        'body': render_template("email_template.html", message=message)
    }
    if request.form['submit'] == "Send":
        task = send_async_email.apply_async(
            args=[email_data], task_id=uuid.uuid4().hex)
    else:
        task = send_async_email.apply_async(args=[email_data], countdown=60)
    return jsonify({}), 202, {"location": url_for('task_status', task_id=task.id)}


@app.route("/tasks/edit-video")
def process_video_get():
    return render_template("edit_video.html")


@app.route("/tasks/edit-video", methods=["POST"])
@limiter.limit("10 per hour")
def process_video():
    if 'file' not in request.files:
        return jsonify({'error': "No file part"}), 204
    file = request.files["file"]
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 204
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = app.config["UPLOAD_FOLDER"]
        file.save(os.path.join(filepath, filename))
        options = request.form.to_dict()
        task = async_process_video.apply_async(
            args=[filepath, filename, options], task_id=uuid.uuid4().hex)
        return jsonify({}), 202, {"location": url_for('task_status', task_id=task.id,
                                                      result=filename)}


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], "PROCESSED_" + filename)
