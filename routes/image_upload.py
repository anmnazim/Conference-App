import os
from flask import Blueprint, request, jsonify, current_app, render_template
from werkzeug.utils import secure_filename

image_bp = Blueprint("image", __name__, template_folder="../templates")

UPLOAD_ROOT = "uploads"

# ---------------- STUDENT UPLOAD ----------------
@image_bp.route("/upload", methods=["POST"])
def upload_image():
    name = request.form.get("name")
    course = request.form.get("course")
    image = request.files.get("image")

    if not all([name, course,  image]):
        return jsonify({"error": "All fields required"}), 400

    folder_name = secure_filename(f"{name}")
    student_folder = os.path.join(UPLOAD_ROOT, folder_name)
    os.makedirs(student_folder, exist_ok=True)

    filename = secure_filename(image.filename)
    image_path = os.path.join(student_folder, filename)
    image.save(image_path)

    current_app.mongo.db.students.insert_one({
        "name": name,
        "course": course,
        "image_path": image_path,
        
    })

    return jsonify({"message": "Uploaded successfully"}), 201


# ---------------- Logo VIEW PAGE ----------------
@image_bp.route("/logo", methods=["GET"])
def teacher_page():
    students = list(current_app.mongo.db.students.find())
    return render_template("logo.html", students=students)


# ---------------- APPROVE / REJECT ----------------
@image_bp.route("/update-status", methods=["POST"])
def update_status():
    student_id = request.form.get("id")
    status = request.form.get("status")

    current_app.mongo.db.students.update_one(
        {"_id": current_app.mongo.db.students.ObjectId(student_id)},
        {"$set": {"status": status}}
    )

    return jsonify({"message": "Status updated"})
