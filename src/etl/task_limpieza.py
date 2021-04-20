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
from src.etl.task_almacenamiento import TaskStore
from src.etl.task_almacenamiento_metadata import TaskStoreMeta
import src.pipeline.ingesta_almacenamiento as ial
from src.utils.cleaning import cleaning

# ================================= LUIGI TASK ================================= #

class TaskCleaning(CopyToTable):
    
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
        return {'A':TaskStore(self.bucket, self.prc_path, self.year, self.month, self.day, self.flg_i0_c1),
                'B':TaskStoreMeta(self.bucket, self.prc_path, self.year, self.month, self.day, self.flg_i0_c1)}

    # RDS database connection
    pg = get_pg_service(ks.path)
    user = pg['user']
    password = pg['password']
    host = pg['host']
    port = pg['port']
    database = pg['dbname']
    table = 'procdata.limpieza'

    # RDS database table columns
    columns = [("aka_name", "varchar"), ("license", "varchar"), ("facility_type", "varchar"), ("label_risk", "int"),
               ("zip", "varchar"), ("inspection_date", "date"), ("inspection_type", "varchar"), ("violations_count", "int"),
               ("sin_mnth", "real"), ("cos_mnth", "real"), ("sin_wkd", "real"), ("cos_wkd", "real"), ("label_results", "int")]    
        
    def rows(self):
        
        # Path from S3 client to open data @ S3
        S3_targ = self.input()['A'].path.split("/")
        buck_path = S3_targ[2]
        key_path = '/'.join(S3_targ[3:])

        # Create a DataFrame from S3 data
        s3 = ial.get_s3_resource()
        datos = s3.meta.client.get_object(Bucket = buck_path, Key = key_path)
        body = datos['Body'].read()
        data_pkl = pickle.loads(body)
        json_dump = json.dumps(data_pkl)
        datos_cfi = pd.read_json(json_dump)
        
        
        # Cleaning and Preprocessing of data.
        cleaned_df, nrows_prev, ncols_prev, nrows_after, ncols_after, data_null_prev = cleaning(datos_cfi)
        
        print("\n\n****************\n\n",nrows_prev, ncols_prev, nrows_after, ncols_after, data_null_prev)

        # Lineage. Creating Metadata @ .csv file
        str_date = str(datetime.date(datetime(self.year, self.month, self.day)))
           
        str_file_csv = str_date + ".csv"
        output_path = "src/temp/metadata/limpieza/type={}/".format(self.flg_i0_c1)
        os.makedirs(output_path, exist_ok = True)
        
        # WORKING
        
        dic_par = {'year':str(self.year),'month':str(self.month),'day':str(self.day),'flg_i0_c1':str(self.flg_i0_c1)}
        
        df = pd.DataFrame({'exec_date': [self.todate], 'exec_param': [json.dumps(dic_par)],'executer': ['luigi'],
                           'source_path': [self.input()['A'].path], 'nrows_prev': [nrows_prev], 'ncols_prev': [ncols_prev],
                           'nrows_after': [nrows_after], 'ncols_after': [ncols_after],'nulls': [data_null_prev]})
        
        df.to_csv(output_path + str_file_csv, index=False, header=False)

        # Write to cleaned data to RDS procdata.limpieza table
        #print("\n\n<<<<<<<<<<<<<<<<<<<<<<<<<<<\n\n",cleaned_df.shape)
        for row in cleaned_df.itertuples(index = False):
            yield row





