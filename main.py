import os
import re
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, flash, redirect, url_for

LAST_IMAGE          = []
UPLOAD_FOLDER       = './static/upload'
ALLOWED_EXTENSIONS  = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__, static_url_path = '')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_file_no(filename):
    name = filename.rsplit('.', 1)
    if name[1] in ALLOWED_EXTENSIONS:
        if re.match("img", name[0]):
            return int(name[0].rsplit('-', 1)[1])


def rename_file():
    file_number = -1
    all_files = os.listdir(UPLOAD_FOLDER)
    for each_name in all_files:
        curr_number = get_file_no(each_name)
        if curr_number is not None and curr_number > file_number:
            file_number = curr_number
    dst_file_name = "img-" + str(file_number+1)
    return dst_file_name


@app.route('/')
@app.route('/root/')
@app.route('/index/')
@app.route('/home/')
def root():
    file_number = -1
    file_ext = []
    all_files = os.listdir(UPLOAD_FOLDER)
    for each_name in all_files:
        curr_number = get_file_no(each_name)
        if curr_number is not None and curr_number > file_number:
            file_number = curr_number
            file_ext = each_name.rsplit('.', 1)[1]
    latest_file_name = "upload/img-" + str(file_number) + "." + str(file_ext)
    print(latest_file_name)
    return render_template('home.html', last_image=latest_file_name)


@app.route('/upload/', methods=['GET', 'POST'])
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print("New file uploaded! ")
            print(filename)
            new_name = rename_file() + "." + str(filename.split('.')[1])
            LAST_IMAGE = os.path.join(app.config['UPLOAD_FOLDER'], new_name)
            print("New name: " + LAST_IMAGE)
            file.save(LAST_IMAGE)
    return render_template('upload.html')


if __name__ == "__main__":
    app.run(debug=True, port=80, host="0.0.0.0")
