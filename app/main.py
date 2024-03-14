
from util import Util
from connection import Connection
from dotenv import load_dotenv
import os
from flask import Flask, render_template





if __name__ == '__main__':

    util = Util('document','json','./')
    archivos_filtrados, directorio = util.busqueda_archivo()
    datafrem_lectura = util.leer_archivo_individual(archivos_filtrados,directorio)
