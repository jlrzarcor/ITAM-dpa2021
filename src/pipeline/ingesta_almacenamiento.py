import boto3
from sodapy import Socrata
from src.utils.general import get_api_token, get_s3_credentials

socrata_domain = "data.cityofchicago.org"
socrata_ds_id = "4ijn-s7e5"

# ================================= FUNCTION 1 ================================= #

def get_client():
    token = get_api_token('../../conf/local/credentials.yaml')
    #token = get_api_token('/mnt/c/Users/jlrza/jlrzcdir/2-data-product-architecture/rep-dpa-proy/conf/local/credentials.yaml')
    client = Socrata(socrata_domain, token['api_token'])  #timeout=10)
    
    return client


# ================================= FUNCTION 2 ================================= #

def ingesta_inicial(client, limit = 300000):
    return client.get(socrata_ds_id, limit = limit)


# ================================= FUNCTION 3 ================================= #
def get_s3_resource():
    #s3_credentials = get_s3_credentials('../../conf/local/credentials.yaml')
    s3_credentials = get_s3_credentials('/mnt/c/Users/jlrza/jlrzcdir/2-data-product-architecture/rep-dpa-proy/conf/local/credentials.yaml')
    
    session = boto3.Session(
        aws_access_key_id = s3_credentials['aws_access_key_id'],
        aws_secret_access_key = s3_credentials['aws_secret_access_key']
    )
    
    s3 = session.resource('s3')
    
    return s3


# ================================= FUNCTION 4 ================================= #

def guardar_ingesta(bucket, bucket_path, data):
    
    
    pass


# ================================= FUNCTION 5 ================================= #

def ingesta_consecutiva(cliente, fecha = '2015-01-04T00:00:00.000', limit = 1000):
    return client.get(socrata_ds_id, where="inspection_date > " + fecha, limit = limit)
