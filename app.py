from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

from routes.image_upload import image_bp

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = os.getenv("MONGO_URI")

if not app.config["MONGO_URI"]:
    raise RuntimeError("MONGO_URI not set")

mongo = PyMongo(app)
app.mongo = mongo

app.register_blueprint(image_bp, url_prefix="/api")

@app.route("/uploads/<path:filename>")
def serve_image(filename):
    return send_from_directory("uploads", filename)

@app.route("/")
def home():
    return {"message": "Backend running"}

if __name__ == "__main__":
      app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
   
