# ================================= LIBRARIES  ================================= #

import yaml

# ================================= FUNCTION 1 ================================= #

def read_yaml(credentials_file):
    """
    Carga las credenciales que se tengan en el archivo especificado.
        
    inputs: 
        credentials_file: archivo con extensión .yaml
    outputs:
        Diccionario con las credenciales de la API de Chicago y de AWS
    """
    
    config = None
    try: 
        with open (credentials_file, 'r') as f:
            config = yaml.safe_load(f)
    except:
        raise FileNotFoundError('Couldnt load the file')
    
    return config


# ================================= FUNCTION 2 ================================= #

def get_s3_credentials(credentials_file):
    """
    Lee el archivo credentials.yaml y devuelve las credenciales 
    del cliente designado para conectarse al servicio s3 de AWS.
    Se requiere que el archivo credentials.yaml contenga:
    s3:
      AWSAccessKeyId= -tu id-
      AWSSecretKey= -tu llave-
    
    inputs:
        credentials_file: archivo con extensión .yaml
    outputs:
        Diccionario con las credenciales de AWS
    """
    s3_credentials = read_yaml(credentials_file)['s3']
    
    return s3_credentials


# ================================= FUNCTION 3 ================================= #

def get_api_token(credentials_file):
    """
    Lee el archivo credentials.yaml y devuelve las credenciales 
    del cliente designado para conectarse al servicio de la API 
    de Chicago Food Inspections.
    Se requiere que el archivo credentials.yaml contenga la siguiente 
    información:
    food_inspections:
        AppToken= -tu Token público-
        SecretToken= -tu Token secreto-
    
    inputs:
        credentials_file: archivo con extensión .yaml
    outputs:
        Diccionario con las credenciales de la API de Chicago food inspections
    """
    
    token = read_yaml(credentials_file)['food_inspections']
    
    return token


# ================================= FUNCTION 4 ================================= #

def get_pg_service(credentials_file):
    """
    Lee el archivo credentials.yaml y devuelve las credenciales 
    del Role de RDS para la base de Chicago Food Inspections.
    Se requiere que el archivo credentials.yaml contenga la siguiente 
    información:
    pg_service:
        user= -docstring-
        password= -docstring-
        host= -docstring-
        port= 5432
        dbname= -docstring-
    
    inputs:
        credentials_file: archivo con extensión .yaml
    outputs:
        Diccionario con las credenciales de la RDS
    """
    
    pg_service = read_yaml(credentials_file)['pg_service']
    
    return pg_service



# ================================= FUNCTION 5 ================================= #

def get_db_conn_sql_alchemy(credentials_file):
    """
    Lee el archivo credentials.yaml y devuelve las credenciales 
    del string para conectar con SQLAlchemy.
    Se requiere que el archivo credentials.yaml contenga la siguiente 
    información:
    sql_alchemy:
        string= -docstring-
    
    inputs:
        credentials_file: archivo con extensión .yaml
    outputs:
        Diccionario con las credenciales SQLAlchemy
    """
    
    sql_alchemy = read_yaml(credentials_file)['sql_alchemy']
    
    return sql_alchemy['conn']
