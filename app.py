from flask import Flask, request, jsonify, send_from_directory, render_template
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from utils.pdf_generator import create_daily_log_pdf

app = Flask(__name__, static_folder="static", static_url_path="/static")

UPLOAD_FOLDER = "static/uploads"
GENERATED_FOLDER = "static/generated"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["GENERATED_FOLDER"] = GENERATED_FOLDER

# ROUTE: Health check
@app.route("/")
def index():
    return "✅ Daily Log AI is running"

# ROUTE: Ping test
@app.route("/ping")
def ping():
    return "PONG"

# ROUTE: Serve static generated PDFs
@app.route("/generated/<filename>")
def serve_pdf(filename):
    try:
        return send_from_directory(app.config["GENERATED_FOLDER"], filename)
    except FileNotFoundError:
        return "PDF not found", 404

# ROUTE: Upload images and generate report
@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.form.to_dict()
        images = request.files.getlist("images")
        logo = request.files.get("logo")
        
        image_paths = []
        for image in images:
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                image.save(path)
                image_paths.append(path)

        logo_path = None
        if logo and allowed_file(logo.filename):
            filename = secure_filename("logo_" + logo.filename)
            logo_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            logo.save(logo_path)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{data.get('project_name', 'daily_log')}_Report_{timestamp}.pdf"
        output_path = os.path.join(app.config["GENERATED_FOLDER"], filename)

        create_daily_log_pdf(data, image_paths, logo_path, output_path)
        
        return jsonify({"pdf_url": f"/generated/{filename}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ROUTE: Dummy PDF test (optional)
@app.route("/generate-test-pdf", methods=["GET"])
def generate_test_pdf():
    output_dir = app.config["GENERATED_FOLDER"]
    os.makedirs(output_dir, exist_ok=True)
    test_pdf_path = os.path.join(output_dir, "test_upload.pdf")
    with open(test_pdf_path, "wb") as f:
        f.write(b"%PDF-1.4\\n% Dummy test PDF\\n%%EOF")
    return jsonify({"message": "✅ Test PDF created", "pdf_url": "/generated/test_upload.pdf"})

# HELPER: File type check
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# RUN LOCALLY
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
