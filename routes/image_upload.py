import uuid
import os
from flask import Blueprint, request, jsonify, current_app, render_template
from imagekitio import ImageKit

image_bp = Blueprint("image", __name__, template_folder="../templates")

imagekit = ImageKit(
    public_key=os.environ["IMAGEKIT_PUBLIC_KEY"],
    private_key=os.environ["IMAGEKIT_PRIVATE_KEY"],
    url_endpoint=os.environ["IMAGEKIT_URL_ENDPOINT"]
)

# ---------------- STUDENT UPLOAD ----------------
@image_bp.route("/upload", methods=["POST"])
def upload_image():
    name = request.form.get("name")
    course = request.form.get("course")
    image = request.files.get("image")

    if not all([name, course, image]):
        return jsonify({"error": "All fields required"}), 400

    filename = f"students/{uuid.uuid4()}_{image.filename}"

    upload = imagekit.upload_file(
    file=image.read(),
    file_name=filename
)

    image_url = upload.url

    current_app.mongo.db.students.insert_one({
        "name": name,
        "course": course,
        "image_url": image_url
    })

    return jsonify({
        "message": "Uploaded successfully",
        "image_url": image_url
    }), 201


# ---------------- LOGO VIEW PAGE ----------------
@image_bp.route("/logo", methods=["GET"])
def teacher_page():
    students = list(current_app.mongo.db.students.find())
    return render_template("logo.html", students=students)
