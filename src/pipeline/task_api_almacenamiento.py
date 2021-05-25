# ================================= LIBRARIES  ================================= #

# importing packages
import luigi
import json
import boto3
import pickle
import pandas as pd
import psycopg2
import yaml
import os

# importing especific functions
from luigi.contrib.postgres import CopyToTable
from luigi.contrib.s3 import S3Target
from datetime import datetime
from io import BytesIO

# importing custom libraries
import src.utils.constants as ks
from src.utils.general import get_pg_service
import src.pipeline.ingesta_almacenamiento as ial

# Requires...
from src.etl.task_predicciones import TaskPredict
from src.etl.task_predicciones_metadata import TaskPredictMeta

# ================================= LUIGI TASK ================================= #

class TaskAPIData(CopyToTable):
    
 # Variables
    # Transfer required variables
    bucket = luigi.Parameter(default = "data-product-architecture-equipo-5")
    prc_path = luigi.Parameter(default = "ingestion")

    # luigi parameters
    todate = datetime.date(datetime.today())        
    year = luigi.IntParameter(default = todate.year)
    month = luigi.IntParameter(default = todate.month)
    day = luigi.IntParameter(default = todate.day)
    
    flg_i0_c1 = luigi.IntParameter(default = 1)    
    
    def requires(self):
        return {'A':TaskPredict(self.bucket, self.prc_path, self.year, self.month, self.day, self.flg_i0_c1),
                'B':TaskPredictMeta(self.bucket, self.prc_path, self.year, self.month, self.day, self.flg_i0_c1)}

 # RDS database connection
    pg = get_pg_service(ks.path)
    user = pg['user']
    password = pg['password']
    host = pg['host']
    port = pg['port']
    database = pg['dbname']
    table = 'api.scores'

 # RDS database table columns
    columns = [("ingest_date", "date"), ("index", "int"), ("aka_name", "varchar"), ("license", "varchar"),
               ("score", "real"), ("prediction", "int")]
        
    def rows(self):

        str_date = str(datetime.date(datetime(self.year, self.month, self.day)))
        
     # Path from S3 client to open data @ S3
        S3_targ = self.input()['A'].path.split("/")
        buck_path = S3_targ[2]
        key_path = '/'.join(S3_targ[3:])

     # Create a DataFrame from S3 data
        s3 = ial.get_s3_resource()
        datos = s3.meta.client.get_object(Bucket = buck_path, Key = key_path)
        body = datos['Body'].read()
        data_pkl = pickle.loads(body)
        datos_cfi = pd.DataFrame(data_pkl)
        datos_cfi.insert(0, "ingest_date", datetime.date(datetime(self.year, self.month, self.day)))
        
        print(datos_cfi.head(3))
        
     # Write predictions to RDS API table
        for row in datos_cfi.itertuples(index = False):
            yield row


