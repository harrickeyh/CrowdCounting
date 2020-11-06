import os

from flask import jsonify
from flask import Flask, render_template, request, redirect, url_for
from predict import get_prediction #Get prediction inference.py
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './static/'
ALLOWED_EXTENSIONS = set(['.jpg', '.jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/implement.html')
def implement():
    '''if request.method == 'POST':         #remove this entire if part if not doing fetch
        # Remove existing images in directory
        files_in_dir = os.listdir(app.config['UPLOAD_FOLDER'])
        filtered_files = [file for file in files_in_dir if file.endswith(".jpg") or file.endswith(".jpeg")]
        for file in filtered_files:
            path = os.path.join(app.config['UPLOAD_FOLDER'], file)
            os.remove(path)

        # Upload new file
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']

        if not file:
            return
        
        print("Getting Prediction")
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        prediction, density = get_prediction(file)
        return render_template('impiement.html',)'''
    return render_template('implement.html')

@app.route('/others.html')
def others():
    return render_template('others.html')


# Remove ''' below to try to use my code for fetch
@app.route('/predict', methods=["GET","POST"])          
def predict():
    if request.method == 'POST':
        # Remove existing images in directory
        files_in_dir = os.listdir(app.config['UPLOAD_FOLDER'])
        filtered_files = [file for file in files_in_dir if file.endswith(".jpg") or file.endswith(".jpeg")]
        for file in filtered_files:
            path = os.path.join(app.config['UPLOAD_FOLDER'], file)
            os.remove(path)
            print("FIle remove")

        # Upload new file
        if 'file' not in request.files:
            print("not in file")
            return redirect(request.url)
        file = request.files['file']

        if not file:
            print("not file")
            return
        
        print("Getting Prediction")
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        prediction, density = get_prediction(file)
    
        return jsonify(prediction, density)

if __name__ == '__main__':
    app.run(debug=True)

## end of line 1