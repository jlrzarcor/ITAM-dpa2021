# ================================= LIBRARIES  ================================= #

import os
import boto3
import pickle as pkl
from sodapy import Socrata
from datetime import datetime

from src.utils.general import get_api_token, get_s3_credentials

# Variables de entorno que se cargan por default al cargar la librería
# ingesta_almacenamiento.py

socrata_domain = "data.cityofchicago.org"
socrata_ds_id = "4ijn-s7e5"
path = os.path.realpath('conf/local/credentials.yaml')

# ================================= FUNCTION  ================================= #

def get_client():
    '''
    Función que recoge el Token de la API Chicago food inspections (contenida
    en el archivo credencials.yaml), se conecta a ella y devuelve el cliente
    con el que se harán las consultas.
        
    outputs:
        Cliente para conectarse a la API Chicago food inspections
    '''
    
    token = get_api_token(path)
    client = Socrata(socrata_domain, token['api_token'])  #timeout=10)
    
    return client

# ================================= FUNCTION 2 ================================= #

def ingesta_inicial(client, limit = 300000):
    '''
    Función que utiliza el cliente de la API Chicago food inspections, realiza
    una consulta histórica de tamaño "limit" y devuelve una lista con los resultados
    de la consulta. Si no hay ese número de registros devolverá el máximo que 
    encuentre en la BD.
    
    inputs:
        client: objeto con el cliente para conectarse a la API Chicago food inspections
        limit: integer con el máximo de registros a consultar
    outputs:
        Lista con el resultado de la consulta inicial (histórica) a la BD
    '''
    return client.get(socrata_ds_id, limit = limit)

# ================================= FUNCTION 3 ================================= #

def get_s3_resource():
    '''
    Función que se crea un objeto "s3" para conectarse al servicio s3 de AWS
    a partir de las crdenciales que se encuentran en credentials.yaml
    
    outputs:
        Objeto s3 de AWS
    '''
    s3_credentials = get_s3_credentials(path)
    session = boto3.Session(
        aws_access_key_id = s3_credentials['aws_access_key_id'],
        aws_secret_access_key = s3_credentials['aws_secret_access_key']
    )
    
    s3 = session.resource('s3')
    
    return s3

# ================================= FUNCTION 4 ================================= #

def guardar_ingesta(my_bucket, bucket_path, data):
    '''
    Función que recibe de argumentos el nombre del bucket s3 en el que se quiere 
    almacenar la consulta, la ruta en la que se guardará la información que se consulte 
    de la API Chicago food inspections y la consulta que se haya realizado previamente
    (inicial o consecutiva). Pueden existir dos casos:
    
        bucket_path = ingestion/initial/:
         Se hará la consulta de todo lo que se encuentre en la BD, desde la fecha en
         que se corre la función y hasta el valor de registros que se estableció 
         en la variable -limit- de la función -ingesta_inicial-.
    
        bucket_path = ingestion/consecutive/:
         Se hará la consulta de todo lo que se encuentre en la BD, desde la fecha que se
         establezca en la variable -delta_date- y hasta el valor de registros que se estableció 
         en la variable -limit- de la función -ingesta_consecutiva-.
     
    inputs:
        my_bucket: string con el nombre del bucket
        bucket_path: string con la ruta donde se guardaran los datos en el bucket
        data: lista con la consulta realizada
    outputs:
        Almacenamiento en el bucket de s3 de la consulta realizada
    '''
    
    s3 = get_s3_resource()
    pickle_buffer = pkl.dumps(data)
    fecha = str(datetime.date(datetime.now()))
    
    if bucket_path == "ingestion/initial":
        nom_file = "ingestion/initial/" + "historic-inspections-" + fecha + ".pkl"
    else:
        nom_file =  "ingestion/consecutive/" + "consecutive-inspections-" + fecha + ".pkl"
    
    s3.Object(my_bucket, nom_file).put(Body = pickle_buffer) 
    return


# ================================= FUNCTION 5 ================================= #

def ingesta_consecutiva(client, delta_date = '2021-02-15T00:00:00.000', limit = 1000):
    '''
    Función que utiliza el cliente de la API Chicago food inspections, realiza 
    una consulta de tamaño "limit" a partir de la fecha establecida en la
    variable -delta_date- y devuelve una lista con los resultados
    de la consulta. Si no hay ese número de registros devolverá el máximo que haya
    en la BD.
    
    inputs:
        client: objeto con el cliente para conectarse a la API Chicago food inspections
        delta_date: date con la fecha desde la cual se desea hacer la consulta
        limit: integer con el número de registros que se desean consultar
    outputs:
        Lista con el resultado de la consulta consecutiva a la BD 
    '''
    
    return client.get(socrata_ds_id, where = "inspection_date > " + "'" + delta_date + "'", limit = limit)
