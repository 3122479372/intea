import pandas as pd
import re
from unidecode import unidecode

class Policy:
    def __init__(self, df):
        self.df = df

    def validar_datos(self):
        if self.df.isnull().values.any():
            print('El DataFrame contiene valores nulos.')   



    def limpiar_datos(self):
        self.df.columns = self.df.columns.str.lower()
        dfe = self.df.applymap(lambda x: x.lower() if isinstance(x, str) else x)
        dfe = dfe.applymap(lambda x: unidecode(x) if isinstance(x, str) else x)
        return dfe






    def aplicar_politicas(self):
        self.validar_datos()
        dfe = self.limpiar_datos()
        return dfe



if __name__ == '__main__':

    df = pd.DataFrame(...)  
    politicas = Policy(df)
    politicas.aplicar_politicas()
