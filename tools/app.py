from flask import Flask, render_template, request, jsonify
import base64, os,csv
from datetime import datetime

app = Flask(__name__)
FILE = "attendance.csv"

# Folder to save incoming images
SAVE_FOLDER = "captured_images"
os.makedirs(SAVE_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')


# Handle form submission
@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name", "").strip()
    roll = request.form.get("roll", "").strip()
    dept = request.form.get("dept", "").strip()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if name and roll and dept:
        file_exists = os.path.exists(FILE)
        with open(FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Name", "Roll", "Department", "Timestamp"])
            writer.writerow([name, roll, dept, timestamp])
        return jsonify({"status": "success", "name": name})
    return jsonify({"status": "error"}), 400


@app.route('/capture', methods=['POST'])
def capture():
    data = request.get_json()
    image_data = data.get('image')

    if not image_data:
        return jsonify({"error": "No image data received"}), 400

    # Remove data URL prefix
    image_data = image_data.split(",")[1]
    image_bytes = base64.b64decode(image_data)

    # Create timestamp-based filename
    filename = datetime.now().strftime("%Y%m%d_%H%M%S_%f") + ".png"
    filepath = os.path.join(SAVE_FOLDER, filename)

    # Save image
    with open(filepath, "wb") as f:
        f.write(image_bytes)

    print(f"[INFO] Saved image: {filepath}")
    return jsonify({"message": "Image saved", "filename": filename})



if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
