import io
import uuid
import os
from flask import Blueprint, request, jsonify, current_app, render_template
from googleapiclient.http import MediaIoBaseUpload
from routes.firebase_service import get_bucket

image_bp = Blueprint("image", __name__, template_folder="../templates")



@image_bp.route("/upload", methods=["POST"])
def upload_image():
    name = request.form.get("name")
    course = request.form.get("course")
    image = request.files.get("image")

    if not all([name, course, image]):
        return jsonify({"error": "All fields required"}), 400

    bucket = get_bucket()

    filename = f"students/{uuid.uuid4()}_{image.filename}"
    blob = bucket.blob(filename)

    blob.upload_from_file(image, content_type=image.mimetype)
    blob.make_public()

    image_url = blob.public_url

    current_app.mongo.db.students.insert_one({
        "name": name,
        "course": course,
        "image_url": image_url
    })

    return jsonify({
        "message": "Uploaded successfully",
        "image_url": image_url
    }), 201
@image_bp.route("/logo", methods=["GET"])
def teacher_page():
    students = list(current_app.mongo.db.students.find())
    return render_template("logo.html", students=students)