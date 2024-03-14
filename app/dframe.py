
import pandas as pd


class Dframe():
    
    def __init__(self,ruta_del_archivos):
        self.ruta_del_archivos = ruta_del_archivos
        
        
    def lectura(self):
        ruta_del_archivos = self.ruta_del_archivos
        # df = pd.read_csv(ruta_del_archivos)
        df = pd.read_json(ruta_del_archivos)
        cabe = df.head()
        print(cabe)
        return df
