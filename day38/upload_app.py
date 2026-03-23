import os
from flask import Flask, request, redirect, url_for, render_template, flash

app = Flask(__name__)
app.secret_key = 'secret123'

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'txt', 'csv', 'pdf', 'png', 'jpg', 'xlsx'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('ファイルが選択されていません')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('ファイルが選択されていません')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))
            flash(f'「{file.filename}」をアップロードしました！')
            return redirect(url_for('index'))
        else:
            flash('許可されていないファイル形式です')
            return redirect(request.url)

    # アップロード済みファイル一覧
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('upload.html', files=files)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
