from flask import Flask
from flask import request
from flask import redirect, url_for, render_template
#from werkzeug import secure_filename
import shutil
import os
import string
import random
import DBConnector


app = Flask(__name__)
app.config.from_object(__name__)

UPLOAD_FOLDER = '/home/kiran/Desktop/cmpe 295A/Final Project/AFS & Dejavu/Automated_Music_Transcription-master/static/sheet_notes/'
ALLOWED_EXTENSIONS = set(['wav','pdf'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def generate_random_name(extension):
    random_name = ''.join(random.SystemRandom().choice(
        string.ascii_lowercase + string.digits) for _ in range(8))
    return random_name + '.' + extension


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET','POST'])
def main():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            filename = file.filename
            DBConnector.insertEntryTODB(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('main.html', filename=filename[:-4])
    else:
        return render_template('main.html')


@app.route('/<filename>')
def display_sheet_notes(filename):
    pdfFile = DBConnector.fetchPdf(filename)
    #pdfFile.save(os.path.join(app.config['UPLOAD_FOLDER'], pdfFile))
    sourcePath = "/home/kiran/Desktop/cmpe 295A/Final Project/AFS & Dejavu/Automated_Music_Transcription-master/%s" % (pdfFile)
    print "%s" % sourcePath 
    destPath = "/home/kiran/Desktop/cmpe 295A/Final Project/AFS & Dejavu/Automated_Music_Transcription-master/static/sheet_notes/%s" % (pdfFile)
    print "%s" % destPath 
    shutil.move(sourcePath, destPath)
    return render_template('display_sheet_notes.html',
                           filename=pdfFile)


if __name__ == "__main__":
    app.run(host='localhost', port=8081, debug=True)
