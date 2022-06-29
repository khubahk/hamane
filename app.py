#app.py
from flask import Flask, flash, request, redirect, url_for, render_template
from prediction import predict
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
 
app = Flask(__name__)
 
UPLOAD_FOLDER = 'static/uploads/'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route("/hasil", methods=['GET','POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            f_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(f_url)
            print('upload_image filename: ' + f_url)
            flash('Image successfully uploaded and displayed below')
            #start prediction
            result = predict(f_url)
            # show = res[1]
            #file_upload =FileSystemStorage()

            return render_template('result.html' ,filename=filename,  result = result)
        else:
            flash('Allowed image types are - png, jpg, jpeg, gif')
            return redirect(request.url)
    #return render_template('hasil.html')
        
         
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run()
