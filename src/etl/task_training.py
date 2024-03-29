# importing packages
import luigi
import luigi.contrib.s3

import json
import os
import pickle as pkl
import pandas as pd
import yaml

import pandas.io.sql as sqlio
import psycopg2

# importing especific functions
from datetime import datetime

# importing custom libraries
import src.utils.constants as ks
from src.utils.general import get_pg_service
import src.pipeline.ingesta_almacenamiento as ial

# Requires...
from src.etl.task_feature_engineering import TaskFeatEng
from src.etl.task_feature_engineering_metadata import TaskFeatEngMeta
from src.utils.training import train

# ================================= LUIGI TASK ================================= #


class TaskTrain(luigi.Task):
    
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
        return {'A':TaskFeatEng(self.bucket, self.prc_path, self.year, self.month, self.day, self.flg_i0_c1),
                'B':TaskFeatEngMeta(self.bucket, self.prc_path, self.year, self.month, self.day, self.flg_i0_c1)}
  
    def run(self):

        str_date = str(datetime.date(datetime(self.year, self.month, self.day)))        
        
      # Create a DataFrame from clean data from RDS db.
        conn = psycopg2.connect(dbname = self.input()['A'].database, user = self.input()['A'].user, password = self.input()['A'].password,
                                port = self.input()['A'].port, host = self.input()['A'].host)
        
        str_qry = "SELECT * FROM procdata.feat_eng WHERE ingest_date between '2010-01-01' and '" + str_date + "';"
        feat_eng_df = sqlio.read_sql_query(str_qry, conn)
        feat_eng_df.drop(columns = ['ingest_date', 'aka_name', 'license'] , inplace=True, errors='raise')
        
      # Apply Training to data.
        df_train_test, nrows_train, nrows_test = train(feat_eng_df)
        
        print("\n\n ======= ======= =======   TRAINING  ======= ======= ======= \n\n\t\t types of: df, nrows train and test and numbers",
              type(df_train_test), type(nrows_train), type(nrows_test), nrows_train, nrows_test, "\n\n")
    
        with self.output().open('w') as f:
            pkl.dump(df_train_test, f)
                    
     # Lineage. Creating Metadata @ .csv file

       # Set path to S3   
        str_file = "training-dataset-" + str_date + ".pkl"
        S3_path = "s3://{}/train/YEAR={}/MONTH={}/DAY={}/{}".\
        format(self.bucket, self.year, self.month, self.day, str_file)        
        
       # Lineage. Creating Metadata @ .csv file
        str_date = str(datetime.date(datetime(self.year, self.month, self.day)))
           
        str_file_csv = str_date + ".csv"
        output_path = "src/temp/metadata/training/type={}/".format(self.flg_i0_c1)
        os.makedirs(output_path, exist_ok = True)
               
        dic_par = {'year':str(self.year),'month':str(self.month),'day':str(self.day),'flg_i0_c1':str(self.flg_i0_c1)}
        df = pd.DataFrame({'exec_date': [self.todate], 'exec_param': [json.dumps(dic_par)],'executer': ['luigi'],
                           'num_regs_str': [len(df_train_test)], 'nrows_train': [nrows_train], 'nrows_test': [nrows_test],
                           'S3_path': [S3_path]})
        df.to_csv(output_path + str_file_csv, index=False, header=False)
                
    def output(self):
    # Formatting date parameters into date-string
        str_date = str(datetime.date(datetime(self.year, self.month, self.day)))

    # Set path to S3   
        str_file = "training-dataset-" + str_date + ".pkl"
        output_path = "s3://{}/train/YEAR={}/MONTH={}/DAY={}/{}".\
        format(self.bucket, self.year, self.month, self.day, str_file)
            
        s3 = ial.get_luigi_s3client()
        return luigi.contrib.s3.S3Target(path = output_path, client = s3, format = luigi.format.Nop)  
    