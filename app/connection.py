from sqlalchemy import create_engine, Column,select, MetaData,types, Table,join,delete,text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
import os

class Connection:
    def __init__(self, nombre_usuario, contraseña, nombre_bd, host='localhost', puerto='5432'):
        self.nombre_usuario = nombre_usuario
        self.contraseña = contraseña
        self.nombre_bd = nombre_bd
        self.host = host
        self.puerto = puerto
        self.cadena_conexion = f'postgresql://{nombre_usuario}:{contraseña}@{host}:{puerto}/{nombre_bd}'
        self.engine = create_engine(self.cadena_conexion)
        self.metadata = MetaData()

    def insertar_autor(self,dataframe):
        dtype = {
            'nombre': types.String,
            'nacionalidad': types.String,
            'fecha_nacimiento': types.String,
            'genero': types.String
            }
        dft = dataframe[['autor_nombre', 'autor_nacionalidad','autor_fecha_nacimiento','autor_genero']]
        dft = dft.rename(columns={'autor_nombre': 'nombre',
                                  'autor_nacionalidad': 'nacionalidad',
                                  'autor_fecha_nacimiento': 'fecha_nacimiento',
                                  'autor_genero': 'genero',
                                  })

        dft.to_sql('autor', con=self.engine, if_exists='append', index=False, dtype=dtype)



    def insertar_editorial(self, dataframe):
        dtype = {
        'nombre_editorial': types.String,
        'ubicacion_editorial': types.String
        }
        dft = dataframe[['nombre_editorial', 'ubicacion_editorial']]
        dft = dft.rename(columns={'nombre_editorial': 'nombre',
                                  'ubicacion_editorial': 'ubicacion',
                                  })
        dft.to_sql('editorial', con=self.engine, if_exists='append', index=False, dtype=dtype,chunksize=1)
        
    def consulta_libreria(self):
        try:
            connection = self.engine.connect()
            self.metadata.reflect(bind=self.engine)
            libro = Table('libro', self.metadata, autoload_with=self.engine)
            autor = Table('autor', self.metadata, autoload_with=self.engine)
            editorial = Table('editorial', self.metadata,  autoload_with=self.engine)
            stmt = select(libro.c.id,libro.c.titulo, 
                          autor.c.nombre.label('nombre_autor'),
                          editorial.c.nombre.label('nombre_editorial'),
                          autor.c.genero,libro.c.isbn,libro.c.precio,libro.c.cantidad_stock) \
            .select_from(
            join(libro, autor, libro.c.id_autor == autor.c.id_autor)
            .join(editorial, libro.c.id_editorial == editorial.c.id_editorial)
    )
            resultado = connection.execute(stmt)
            column_names = resultado.keys()
            rows = [dict(zip(column_names, row)) for row in resultado.fetchall()]
            # json_result = json.dumps(rows)
            print(rows)
            return rows
        except Exception as ex:
            print('01. Error consulta: '+str(ex))
        
    def consulta_id(self,autor_libro,nombre_editorial):

        connection = self.engine.connect()
        self.metadata.reflect(bind=self.engine)
        autor = Table('autor', self.metadata, autoload_with=self.engine)
        editorial = Table('editorial', self.metadata,  autoload_with=self.engine)
        
        
        stmt = select(autor.c.id_autor, editorial.c.id_editorial) \
                .select_from(autor.join(editorial, editorial.c.nombre == nombre_editorial)) \
                .where(autor.c.nombre == autor_libro)
        resultado = connection.execute(stmt).fetchall()
        print(resultado)
        return resultado
                    
    def insertar_libro(self, dataframe):

        for index, row in dataframe.iterrows():
            print(type(row))
            # print(dataframe[index])
            print(row['autor_nombre'])
            print(row['nombre_editorial'])
            consulta_a_id =self.consulta_id(row['autor_nombre'],row['nombre_editorial'])
            consul = consulta_a_id[0]
            dif = {
                'titulo': row['titulo'],
                'isbn': row['isbn'],
                'precio': row['precio'],
                'cantidad_stock': row['cantidad_stock'],
                'id_editorial': consul[0],
                'id_autor': consul[1],
            }            
            data = pd.DataFrame(dif,index=[index])
            data.to_sql('libro', con=self.engine, if_exists='append', index=False)
        return dataframe
    
    def eliminar_libro(self, id_libro):
        connection = self.engine.connect()
        self.metadata.reflect(bind=self.engine)
        libro = Table('libro', self.metadata, autoload_with=self.engine)
        criterio = libro.c.id == id_libro
        stmt = text(f'DELETE  from libro where id =  :id_libro')
        
       
        with connection as conn:
            resultado = connection.execute(stmt, id_libro)
            print("Filas afectadas:", resultado.rowcount)


if __name__ == "__main__":

    base_de_datos = Connection('postgres', 'ibio', 'libreria')
    base_de_datos.eliminar_libro(32)
