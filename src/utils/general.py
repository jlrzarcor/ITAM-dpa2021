# ================================= LIBRARIES  ================================= #

import yaml

# ================================= FUNCTION 1 ================================= #

def read_yaml(credentials_file):
    """ Carga las credenciales que se tengan en el path especificado,
        para esta  aplicación se debe colocar en la ruta:
        /conf/local/credentials.yaml
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
    """ Lee el archivo credentials.yaml y devuelve las credenciales 
        del cliente designado para conectarse al servicio s3 de AWS.
        Se requiere que el archivo credentials.yaml contenga:
        s3:
        AWSAccessKeyId= -tu id-
        AWSSecretKey= -tu llave-
    """
    s3_credentials = read_yaml(credentials_file)['s3']
    
    return s3_credentials


# ================================= FUNCTION 3 ================================= #

def get_api_token(credentials_file):
    """ Lee el archivo credentials.yaml y devuelve las credenciales 
        del cliente designado para conectarse al servicio de la API 
        de Chicago Food Inspections.
        Se requiere que el archivo credentials.yaml contenga la siguiente 
        información:
        food_inspections:
        AppToken= -tu Token público-
        SecretToken= -tu Token secreto-
        """
    token = read_yaml(credentials_file)['food_inspections']
    
    return token
