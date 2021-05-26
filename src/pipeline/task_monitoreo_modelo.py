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
import pandas.io.sql as sqlio
from pandas.io import sql
from luigi.contrib.postgres import CopyToTable
from luigi.contrib.s3 import S3Target
from datetime import datetime
from io import BytesIO

# importing custom libraries
import src.utils.constants as ks
from src.utils.general import get_pg_service
import src.pipeline.ingesta_almacenamiento as ial

# Requires...
from src.pipeline.task_api_almacenamiento import TaskAPIData
from src.etl.task_predicciones import TaskPredict

# ================================= LUIGI TASK ================================= #

# IMPORTANT REVIEW: --->>> Import Model Scores from AWS-S3 stored @biasandfairness. As We expect scores from model preidctions and we can´t persist twice in a single luigi task, We decided to persist model-scores into same S3 path as biasnand fairnes, thus We could be able to track it for deployment with metadata.biasfair table.



class TaskDashData(CopyToTable):
    
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
                'B':TaskAPIData(self.bucket, self.prc_path, self.year, self.month, self.day, self.flg_i0_c1)}

 # RDS database connection
    pg = get_pg_service(ks.path)
    user = pg['user']
    password = pg['password']
    host = pg['host']
    port = pg['port']
    database = pg['dbname']
    table = 'dsh.model'
    
 # RDS database table columns
    columns = [("ingest_date", "date"), ("type", "varchar"), ("scores", "real")]
        
    def rows(self):

        str_date = str(datetime.date(datetime(self.year, self.month, self.day)))

    # ^ Connection to dsh.model to clear all last_model_predictions for avoiding duplicate data.
      # Path from S3 client to open data @ S3

        pg_aux = get_pg_service(ks.path)
        conn = psycopg2.connect(dbname = pg_aux['dbname'], user = pg_aux['user'], password = pg_aux['password'],
                                port = pg_aux['port'], host = pg_aux['host'])

        from sqlalchemy import create_engine
        engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(pg_aux['user'], pg_aux['password'], 
                                                                    pg_aux['host'] , pg_aux['port'], pg_aux['dbname']))
        str_qry = "DELETE FROM dsh.model WHERE type = 'm';"
        sql.execute(str_qry, engine)
        
        
        
    # ^ Connection to Open last set of Predictions
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



    # ^ RDS database connection to get S3 last model path 

        pg_aux = get_pg_service(ks.path)
        conn = psycopg2.connect(dbname = pg_aux['dbname'], user = pg_aux['user'], password = pg_aux['password'],
                                port = pg_aux['port'], host = pg_aux['host'])
        
        str_qry = "SELECT S3_store_path FROM metadata.biasfair ORDER BY s3_store_path DESC FETCH FIRST ROW ONLY;"
        S3_targ = sqlio.read_sql_query(str_qry, conn)
        
        print("\n\n ======= ======= =======   ENDING PIPELINE.   ======= ======= ======= \n\n")
        print("\t                                   |>                                   ")
        print("\t                                   |                                    ")
        print("\t                                   |                                    ")
        print("\t                   =======   ================   =======                 ")
        print("\t           ======= =======                      ======= =======         ")
        print("\t   ======= ======= =======   ================   ======= ======= ======= ")
        print("\t   ======= ======= =======   ================   ======= ======= ======= ")
        print("\t   ======= ======= =======   ====_______=====   ======= ======= ======= ")
        print("\t   ======= ======= =======   ====|  |  |=====   ======= ======= ======= ")
        print("\t   ======= ======= =======   ====|  |  |=====   ======= ======= ======= ")
        print("\t   ======= ======= =======   ====|  |  |=====   ======= ======= ======= \n\n")
            
      # Path for S3 client to open last model stored @ S3
        S3_targ_splt = S3_targ.iloc[0,0].split("/")
        buck_path = S3_targ_splt[2]
        key_path = '/'.join(S3_targ_splt[3:])
        key_path = key_path.replace('/biasandfair', '/model-scores')
              
      # Load model
        s3 = ial.get_s3_resource()
        datos = s3.meta.client.get_object(Bucket = self.bucket, Key = key_path)
        body = datos['Body'].read()
        df_model_SCORES = pickle.loads(body)
        
        datos_cfi.drop(columns = ['index', 'aka_name', 'license', 'prediction'], inplace=True, errors='raise')
        datos_cfi.insert(1, "type", 'c')
        datos_cfi.rename(columns = {"score":"scores"}, inplace=True)
        
        df_model_SCORES.drop(columns = ['predicted', 'label'], inplace=True, errors='raise')
        ingest_date = S3_targ_splt[7].replace('.pkl', '')
        ingest_date_ok = ingest_date.replace('biasandfair-', '')
        df_model_SCORES.insert(0, "ingest_date", ingest_date_ok)
        df_model_SCORES.insert(1, "type", 'm')

        scores_dash = pd.concat([datos_cfi, df_model_SCORES], axis = 0)
        
    # ^ Write predictions to RDS dsh.model table
        for row in scores_dash.itertuples(index = False):
            yield row


