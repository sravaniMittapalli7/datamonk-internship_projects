from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import sqlite3
import boto3
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_REGION = os.getenv('AWS_REGION')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

# ✅ Initialize Flask app
app = Flask(__name__)

# ✅ Set up CORS for localhost:5173 (your React dev server)
CORS(app, origins=["http://localhost:5173"], supports_credentials=True)


# SQLite setup (no SQLAlchemy)
DB_PATH = "files.db"
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS file_metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT UNIQUE,
        s3_path TEXT UNIQUE
    )''')
    conn.commit()
    conn.close()


s3 = boto3.resource(
    service_name='s3',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)
bucket = s3.Bucket(AWS_BUCKET_NAME)

def sync_s3_to_sqlite():
    # Clear and repopulate the file_metadata table from S3
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM file_metadata")
    conn.commit()
    for obj in bucket.objects.all():
        file_name = obj.key
        s3_path = obj.key
        print(file_name, s3_path)
        c.execute("INSERT INTO file_metadata (file_name, s3_path) VALUES (?, ?)", (file_name, s3_path))
    conn.commit()
    conn.close()

init_db()
sync_s3_to_sqlite()



@app.route("/list-files", methods=["GET"])
def list_files():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT file_name, s3_path FROM file_metadata")
    files = c.fetchall()
    conn.close()
    return jsonify([{"file_name": f[0], "s3_path": f[1]} for f in files])

@app.route("/upload-file", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"detail": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"detail": "No selected file"}), 400
    try:
        contents = file.read()
        s3_path = file.filename
        bucket.put_object(Key=s3_path, Body=contents)
        # Store metadata in sqlite
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO file_metadata (file_name, s3_path) VALUES (?, ?)", (file.filename, s3_path))
        conn.commit()
        conn.close()
        return jsonify({"message": f"Uploaded {file.filename} to {AWS_BUCKET_NAME}/{s3_path}"})
    except Exception as e:
        return jsonify({"detail": str(e)}), 500

@app.route("/download-file/<file_name>", methods=["GET"])
def download_file(file_name):
    try:
        obj = bucket.Object(file_name)
        file_stream = obj.get()["Body"].read()
        return send_file(
            BytesIO(file_stream),
            as_attachment=True,
            download_name=file_name,
            mimetype="application/octet-stream"
        )
    except Exception as e:
        return jsonify({"detail": str(e)}), 500

@app.route("/delete-file/<file_name>", methods=["DELETE"])
def delete_file(file_name):
    try:
        obj = bucket.Object(file_name)
        obj.load()
        obj.delete()
        # Remove metadata from sqlite
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("DELETE FROM file_metadata WHERE file_name = ?", (file_name,))
        conn.commit()
        conn.close()
        return jsonify({"message": f"Deleted {file_name} from {AWS_BUCKET_NAME}"})
    except Exception as e:
        if hasattr(e, 'response') and getattr(e, 'response', {}).get('Error', {}).get('Code') == '404':
            return jsonify({"detail": f"File '{file_name}' does not exist in {AWS_BUCKET_NAME}."}), 404
        else:
            return jsonify({"detail": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
