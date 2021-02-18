def read_yaml(credentials_file):
    pass

def get_s3_credentials(credentials_file):
    s3_credentials=read_yaml(credentials_file)['s3']
    return s3_credentials

def get_api_token(credentials_file):
    token=read_yaml(credentials_file)['food_inspections']
    return token
