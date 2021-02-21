# ================================= LIBRARIES  ================================= #

import os
import boto3
import pickle as pkl
from sodapy import Socrata
from datetime import datetime

from src.utils.general import get_api_token, get_s3_credentials

socrata_domain = "data.cityofchicago.org"
socrata_ds_id = "4ijn-s7e5"
path = os.path.realpath('conf/local/credentials.yaml')

# ================================= FUNCTION  ================================= #

def get_client():
    token = get_api_token(path)
    #token = get_api_token('/mnt/c/Users/jlrza/jlrzcdir/2-data-product-architecture/rep-dpa-proy/conf/local/credentials.yaml')
    client = Socrata(socrata_domain, token['api_token'])  #timeout=10)
    
    return client


# ================================= FUNCTION 2 ================================= #

def ingesta_inicial(client, limit = 300000):
    return client.get(socrata_ds_id, limit = limit)


# ================================= FUNCTION 3 ================================= #
def get_s3_resource():
    s3_credentials = get_s3_credentials(path)
    #s3_credentials = get_s3_credentials('/mnt/c/Users/jlrza/jlrzcdir/2-data-product-architecture/rep-dpa-proy/conf/local/credentials.yaml')
    
    session = boto3.Session(
        aws_access_key_id = s3_credentials['aws_access_key_id'],
        aws_secret_access_key = s3_credentials['aws_secret_access_key']
    )
    
    s3 = session.resource('s3')
    
    return s3


# ================================= FUNCTION 4 ================================= #

def guardar_ingesta(my_bucket, bucket_path, data):
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
    return client.get(socrata_ds_id, where = "inspection_date > " + "'" + delta_date + "'", limit = limit)
