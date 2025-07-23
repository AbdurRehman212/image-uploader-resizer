from flask import Flask, request, jsonify, render_template, send_file
import os
from werkzeug.utils import secure_filename
from PIL import Image
import boto3
from io import BytesIO
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv(dotenv_path='./.env')

# ✅ AWS credentials from env
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

# ✅ Safety check
print("🔎 AWS_ACCESS_KEY_ID =", AWS_ACCESS_KEY_ID)
if not all([AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, AWS_BUCKET_NAME]):
    raise ValueError("❌ Missing AWS environment variables. Check .env file or Docker --env-file.")

# ✅ Flask App Setup
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# ✅ Allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# ✅ Upload route
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part in the request'}), 400

    file = request.files['image']
    scale = request.form.get('scale', '100')

    if file.filename == '':
        return jsonify({'error': 'No selected image'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Unsupported file type'}), 400

    try:
        # ✅ Secure and resize
        filename = secure_filename(file.filename)
        image = Image.open(file.stream)
        scale_factor = int(scale) / 100.0
        resized = image.resize((int(image.width * scale_factor), int(image.height * scale_factor)))

        # ✅ Buffer image
        buffer = BytesIO()
        resized.save(buffer, format=image.format)
        buffer.seek(0)

        # ✅ Upload to S3
        s3 = boto3.client(
            's3',
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

        s3_key = f"uploads/{filename}"
        s3.upload_fileobj(
            buffer,
            AWS_BUCKET_NAME,
            s3_key,
            ExtraArgs={'ContentType': file.content_type}
        )

        return jsonify({
            'message': f'Image uploaded, resized to {scale}%, and stored in S3.',
            'filename': filename
        })

    except Exception as e:
        return jsonify({'error': f'❌ Upload failed: {str(e)}'}), 500

# ✅ Direct S3 Download Route
@app.route('/download/<filename>')
def download_file(filename):
    try:
        s3_key = f"uploads/{filename}"
        buffer = BytesIO()

        s3 = boto3.client(
            's3',
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

        s3.download_fileobj(AWS_BUCKET_NAME, s3_key, buffer)
        buffer.seek(0)

        return send_file(
            buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='image/png'
        )

    except Exception as e:
        return jsonify({'error': f'Download failed: {str(e)}'}), 500

# ✅ Run app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
