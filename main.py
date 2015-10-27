from flask import Flask
from flask import request
from flask import redirect, url_for, render_template
from werkzeug import secure_filename
import os
import string
import random


app = Flask(__name__)
app.config.from_object(__name__)

UPLOAD_FOLDER = '/Users/SRJN/Desktop/Automated_Music_Transcription-master'
ALLOWED_EXTENSIONS = set(['wav'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def generate_random_name(extension):
    random_name = ''.join(random.SystemRandom().choice(
        string.ascii_lowercase + string.digits) for _ in range(8))
    return random_name + '.' + extension


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            filename = generate_random_name('wav')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('main.html', filename=filename[:-4])
    return render_template('main.html')


@app.route('/<filename>')
def display_sheet_notes(filename):
    return render_template('',
                           filename=filename)


if __name__ == "__main__":
    app.run(host='localhost', port=9091, debug=True)
