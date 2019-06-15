import os #ファイルやディレクトリが使えるようにする
from flask import Flask,request,redirect,url_for,flash
from werkzeug.utils import secure_filename
from flask import send_from_directory

from keras.models import Sequential , load_model #学習済みのファイルを扱うため
import keras,sys
import numpy as np
from PIL import Image

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png','jpg','gif'])

classes = ["vehicle","bike","human"]
num_classes = len(classes)
image_size = 50

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#ファイルアップロードの可否判定
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods = ['GET','POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('ファイルがありません')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('ファイルがありません')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            #出力先を指定
            filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)

            model = load_model('./observed_cnn_epoch=100.h5')

            image = Image.open(filepath)
            image = image.convert('RGB')
            image = image.resize((image_size,image_size))
            data = np.asarray(image)
            X = []
            X.append(data)
            X = np.array(X)

            result = model.predict([X])[0]
            predicted = result.argmax()
            percentage = int(result[predicted]*100)

            return "ラベル: " + classes[predicted] + str(percentage) + " %"

            #return redirect(url_for('uploaded_file',filename=filename))

    return '''
    <!doctype html>
    <html>
    <head>
    <meta charset = "UTF-8">
    <title>ファイルをアップロードして判定しよう</title></head>
     <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

    <body>
    <h1>ファイルをアップロードして判定しよう!</h1>
    <form method = post enctype = multipart/form-data>
    <p><input type=file name=file>
    <input type=submit value=Upload>
    </form>
    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>

    </body>
    </html>
    '''
@app.route('/uploads/<filename>')#ファイルページ用に表示できる
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)
