from src.utils.general import get_token, get s3_credentials

def get_client():
    token=get_token("../../conf/local/credentials.yaml")
    pass

def ingesta_inicial(client, limit):
    pass

def get_s3_resource():
    s3_credentials=get_s3_credentials("../../conf/local/credentials.yaml")
    pass

def guardar_ingesta(bucket, bucket_path, data):
    pass

def ingesta_consecutiva(cliente, fecha, limit):
    pass
