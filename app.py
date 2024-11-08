from src.predict import randomForest
from flask import Flask, request, render_template, flash, redirect, url_for
from dotenv import load_dotenv  # type: ignore
import os

load_dotenv()

app = Flask(__name__)

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            seed = str(int.from_bytes(os.urandom(5), 'big'))
            randomForest(file, 70, seed)
            return redirect(url_for('plot_results', seed=seed))
    return render_template('index.html')


@app.route('/upload/<seed>')
def plot_results(seed):
    return render_template('upload.html',
                           plotURL='/static/images/'+seed+'.png')
