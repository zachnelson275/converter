from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
import os
import uuid
from utils.color_utils import convert_image_to_masks
from utils.vectorize import vectorize_masks_to_svg
from utils.svg_builder import build_svg_from_paths

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], f"{uuid.uuid4()}_{filename}")
            file.save(filepath)

            # 1. Convert image to color masks
            masks, color_map = convert_image_to_masks(filepath)

            # 2. Vectorize masks into SVG paths
            paths = vectorize_masks_to_svg(masks)

            # 3. Build final SVG with layers
            svg_path = os.path.join(PROCESSED_FOLDER, f"{uuid.uuid4()}.svg")
            build_svg_from_paths(paths, color_map, svg_path)

            return send_file(svg_path, as_attachment=True, mimetype="image/svg+xml")

    return render_template("index.html")
