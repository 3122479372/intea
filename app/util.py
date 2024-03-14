import os
from dframe import Dframe
from policy import Policy
from connection import Connection
from dotenv import load_dotenv

class Util:
    
    def __init__(self, nombre_carpeta, extension_archivos, ruta):
        self.nombre_carpeta = nombre_carpeta
        self.extension_archivos = extension_archivos
        self.ruta = ruta
        
    def busqueda_archivo(self):
        try:
            archivos_a_excluir = ["validation.csv"]
            nombre_carpeta = self.nombre_carpeta
            ruta = self.ruta
            extension_archivo = self.extension_archivos
            directorio = os.path.join(f'{ruta}/{nombre_carpeta}')
            elementos = os.listdir(directorio)
            archivos_filtrados = [elemento for elemento in elementos if os.path.isfile(os.path.join(directorio, elemento)) 
                      and elemento.endswith(extension_archivo) and elemento not in archivos_a_excluir]
            return archivos_filtrados, directorio
        except Exception as ex:
            print(str(ex))
            
    def leer_archivo_individual(self,archivos_filtrados, directorio):
        try:
            load_dotenv()
            usuario = os.getenv('NOMBRE_USUARIO')
            contrasena = os.getenv('CONTRASENA_USUARIO')
            db = os.getenv('BD')
            for archivo in archivos_filtrados:
                
                ruta_archivo = os.path.join(directorio, archivo)
                datafreme = Dframe(ruta_archivo)
                lectura_frame=datafreme.lectura()
                politicas = Policy(lectura_frame)
                lectura_politica = politicas.aplicar_politicas()
                base_de_datos = Connection(usuario, contrasena, db)
                # base_de_datos.insertar_autor(lectura_politica)
                # base_de_datos.insertar_editorial(lectura_politica)
                base_de_datos.insertar_libro(lectura_politica)
                dataframe_datos = base_de_datos.consulta_libreria()
                
            # datos_renderizar = dataframe_datos.to_dict(orient='records')
            return dataframe_datos

        except Exception as ex:
            print(str(ex))




if __name__ == '__main__':
    
    util = Util('document','json','./')
    archivos_filtrados, directorio = util.busqueda_archivo()
    datafrem_lectura = util.leer_archivo_individual(archivos_filtrados,directorio)

      
        
        
        
    