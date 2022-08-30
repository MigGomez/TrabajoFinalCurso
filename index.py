import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage



app= Flask(__name__)
app.config['UPLOAD_FOLDER'] = './Archivos excel'
ALLOWED_EXTENSIONS = set(['.xls'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/uploader", methods=['POST'])
def uploader():
    if request.method == 'POST':
        archivos=request.files.getlist('archivos')
        for f in archivos: 
            #f = request.files['archivo']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))
        return render_template("index.html", msg="Archivos cargados correctamente")

    return render_template("index.html", msg="Seleccionar archivos")

@app.route("/obtener", methods=["GET"])
def obtener():


    if request.method == 'GET':
        script='./Script/cinemas.py'
        exec(open(script).read())
    return render_template("index.html", msg2="Datos obtenidos correctamente")

    

if __name__ == '__main__':
    app.run(debug=True)
    
