import yaml

# ================================= FUNCTION 1 ================================= #

def read_yaml(credentials_file):
    """ load yaml cofigurations """
    
    config = None
    try: 
        with open (credentials_file, 'r') as f:
            config = yaml.safe_load(f)
    except:
        raise FileNotFoundError('Couldnt load the file')
    
    return config


# ================================= FUNCTION 2 ================================= #

def get_s3_credentials(credentials_file):
    s3_credentials = read_yaml(credentials_file)['s3']
    
    return s3_credentials


# ================================= FUNCTION 3 ================================= #

def get_api_token(credentials_file):
    
    token = read_yaml(credentials_file)['food_inspections']
    
    return token
