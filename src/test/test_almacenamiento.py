# ================================= LIBRARIES  ================================= #

# importing packages
import pandas as pd
import marbles.core
import pickle
import json
import boto3
from datetime import datetime
import os

# importing especific functions
from luigi.contrib.s3 import S3Target

# importing custom libraries
import src.utils.constants as ks
from src.utils.general import get_pg_service
import src.pipeline.ingesta_almacenamiento as ial

# Requires...

# ================================= FUNCTION: testing DF ================================= #

class TestStoredS3(marbles.core.TestCase):
    
    # Variables
    todate = datetime.date(datetime.today())
    test_meth = ''
    status = ''
    err_msg = ''

    __name__ = 'TestIngest'
    
    def test_num_col(self):
        
        S3_targ = pd.read_csv('src/test/trans_file.csv', header = None).iloc[0,0]
        
        # Path from S3 client to open data @ S3
        S3_targ_splt = S3_targ.split("/")
        buck_path = S3_targ_splt[2]
        key_path = '/'.join(S3_targ_splt[3:])

        # Create a DataFrame from S3 data
        s3 = ial.get_s3_resource()
        datos = s3.meta.client.get_object(Bucket = buck_path, Key = key_path)
        body = datos['Body'].read()
        data_pkl = pickle.loads(body)
        #json_dump = json.dumps(data_pkl). Consider to Remove 
        #datos_cfi = pd.read_json(json_dump). Consider to Remove
        datos_cfi = pd.DataFrame(data_pkl)
        df_sh = datos_cfi.shape
        
        self.assertEqual(df_sh[1], 17, note = "La tabla de ingesta inicial almacedada en AWS S3 no corresponde con el número de columnas esperado.")
        self.status = "TestPassed:)"
        self.test_meth = "test_num_col"
        
        