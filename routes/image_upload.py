import io
import uuid
import os
from flask import Blueprint, request, jsonify, current_app, render_template
from googleapiclient.http import MediaIoBaseUpload
from routes.drive_service import get_drive_service

image_bp = Blueprint("image", __name__, template_folder="../templates")

FOLDER_ID = os.environ["GOOGLE_DRIVE_FOLDER_ID"]

@image_bp.route("/upload", methods=["POST"])
def upload_image():
    name = request.form.get("name")
    course = request.form.get("course")
    image = request.files.get("image")

    if not all([name, course, image]):
        return jsonify({"error": "All fields required"}), 400

    drive_service = get_drive_service()

    filename = f"{uuid.uuid4()}_{image.filename}"

    media = MediaIoBaseUpload(
        io.BytesIO(image.read()),
        mimetype=image.mimetype,
        resumable=True
    )

    uploaded = drive_service.files().create(
        body={
            "name": filename,
            "parents": [FOLDER_ID]
        },
        media_body=media,
        fields="id"
    ).execute()

    file_id = uploaded["id"]

    view_url = f"https://drive.google.com/uc?id={file_id}"
    download_url = f"https://drive.google.com/uc?id={file_id}&export=download"

    current_app.mongo.db.students.insert_one({
        "name": name,
        "course": course,
        "file_id": file_id,
        "view_url": view_url,
        "download_url": download_url
    })

    return jsonify({
        "message": "Uploaded successfully",
        "view_url": view_url
    }), 201
@image_bp.route("/logo", methods=["GET"])
def teacher_page():
    students = list(current_app.mongo.db.students.find())
    return render_template("logo.html", students=students)