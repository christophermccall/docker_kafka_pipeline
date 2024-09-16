from flask import Flask, request, jsonify
import boto3
import os

app = Flask(__name__)

# Initialize the S3 client with your AWS credentials
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_DEFAULT_REGION')
)

BUCKET_NAME = 'your-s3-bucket-name'  # Replace with your actual S3 bucket name

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    try:
        s3.upload_fileobj(file, BUCKET_NAME, file.filename)
        return jsonify({"message": "File uploaded successfully to S3"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/report', methods=['GET'])
def generate_report():
    # Placeholder for report generation logic
    return jsonify({"report": "Daily sales report"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
