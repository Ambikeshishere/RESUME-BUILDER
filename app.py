from flask import Flask, render_template, request, send_from_directory, jsonify
import os
from resume_processing import create_refined_resume

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ----------------------------
# 🔥 Serve Homepage
# ----------------------------
@app.route("/")
def index():
    return render_template("index.html")


# ----------------------------
# 📤 Handle File Upload and Process
# ----------------------------
@app.route("/upload", methods=["POST"])
def upload_file():
    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded."})

    file = request.files["resume"]
    if file.filename == "":
        return jsonify({"error": "No selected file."})

    # Save uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Process the resume and generate DOCX
    docx_filename = create_refined_resume(file_path)

    if docx_filename:
        return jsonify({"file_url": f"/download/{docx_filename}"})
    else:
        return jsonify({"error": "Failed to process the file."})


# ----------------------------
# 📥 Download Refined DOCX
# ----------------------------
@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)


# ----------------------------
# 🧠 Run Flask App
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)
