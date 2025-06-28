import os
import re
from flask import Flask, render_template, request, redirect, url_for, send_file
import qrcode

app = Flask(__name__)

STATIC_FOLDER = 'static'
QR_CODE_DIR = os.path.join(STATIC_FOLDER, 'qrcodes')
app.config['UPLOAD_FOLDER'] = QR_CODE_DIR

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def validate_linkedin_url(url):
    pattern = r'^https:\/\/(www\.)?linkedin\.com\/(in|company)\/[a-zA-Z0-9\-_]+\/?$'
    return re.match(pattern, url) is not None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        linkedin_url = request.form.get('linkedin_url').strip()

        if not validate_linkedin_url(linkedin_url):
            return render_template('index.html', error="Invalid LinkedIn URL.")

        qr_filename = 'linkedin_profile_qr.png'
        qr_path = os.path.join(app.config['UPLOAD_FOLDER'], qr_filename)

        img = qrcode.make(linkedin_url)
        img.save(qr_path)

        return redirect(url_for('qr_display', filename=qr_filename))

    return render_template('index.html')

@app.route('/qr-code')
def qr_display():
    filename = request.args.get('filename', 'linkedin_profile_qr.png')
    qr_url = url_for('static', filename=f'qrcodes/{filename}')
    return render_template('qr_display.html', qr_image=qr_url, filename=filename)

@app.route('/download/<filename>')
def download_qr(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
