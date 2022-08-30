from re import sub
import subprocess
import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage



app= Flask(__name__)
app.config['UPLOAD_FOLDER'] = './Datos Ingresos'
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
5
#este metodo es para el web scraping pero por el momento lo dejaremos comentado si no les va a alterar los
#datos obtenidos este dia y no les van a concordar con los del ing.
''' @app.route("/obtener", methods=["GET"])
def obtener():
    if request.method == 'GET':
        subprocess.call(['python ','Cinepolis Horarios.py'])
    return render_template("index.html", msg2="Datos obtenidos correctamente")
 '''
@app.route("/depurar", methods=["GET"])
def depurar():
    if request.method == 'GET':
        subprocess.call(['python ','Limpiar Datos Ingresos.py'])
    return render_template("index.html", msg3="Datos listos y depurados")
    
if __name__ == '__main__':
    app.run(debug=True)
    
