from flask import Flask, render_template
from util import Util

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    util = Util('document','json','./')
    archivos_filtrados, directorio = util.busqueda_archivo()
    datafrem_lectura = util.leer_archivo_individual(archivos_filtrados,directorio)
    
    print(datafrem_lectura)
    return render_template('index.html', libros=datafrem_lectura)

if __name__ == '__main__':
    app.run(debug=True)
