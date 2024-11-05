from flask import Flask, request, render_template
from dotenv import load_dotenv  # type: ignore

load_dotenv()

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/greet', methods=['POST'])
def requests():
    name = request.form['name']
    return render_template('greet.html', name=name)
