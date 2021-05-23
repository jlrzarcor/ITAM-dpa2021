# importing packages
import luigi # OK 
import luigi.contrib.s3 # OK

import json #REVIEW
import os # OK
import pickle as pkl #OK
import pandas as pd #OK 
import yaml #REVIEW

import pandas.io.sql as sqlio #OK
import psycopg2 #OK

# importing especific functions
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit # REVIEW WITH URIEL
from sklearn.tree import DecisionTreeClassifier # REVIEW WITH URIEL
from datetime import datetime #OK

# importing custom libraries
import src.utils.constants as ks #OK
from src.utils.general import get_pg_service #OK
import src.pipeline.ingesta_almacenamiento as ial #OK

# Requires...
from src.etl.task_feature_engineering import TaskFeatEng #OK
from src.etl.task_feature_engineering_metadata import TaskFeatEngMeta #OK

# ============================= IMPORTANT REMINDER ====================

from src.utils.predict import predict

# ================================= LUIGI TASK ================================= #


class TaskPredict(luigi.Task):
    
 # Declare Parameters

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
        return {
                'A':TaskFeatEng(self.bucket, self.prc_path, self.year, self.month, self.day, self.flg_i0_c1),
                'B':TaskFeatEngMeta(self.bucket, self.prc_path, self.year, self.month, self.day, self.flg_i0_c1)
               }
    
    def run(self):

        str_date = str(datetime.date(datetime(self.year, self.month, self.day)))
        
    # ^ RDS database connection to get S3 last model path 

        pg_aux = get_pg_service(ks.path)
        conn = psycopg2.connect(dbname = pg_aux['dbname'], user = pg_aux['user'], password = pg_aux['password'],
                                port = pg_aux['port'], host = pg_aux['host'])
        
        str_qry = "SELECT S3_store_path FROM metadata.modelo ORDER BY exec_date LIMIT 1;"
        S3_targ = sqlio.read_sql_query(str_qry, conn)
        print("\n\n ======= ======= =======   ruta modelo en S3 para predicciones   ======= ======= ======= \n\n", S3_targ.iloc[0,0],"\n\n")
        
    # ^ Import Selected Model from AWS-S3
        # Path for S3 client to open last model stored @ S3
        S3_targ_splt = S3_targ.iloc[0,0].split("/")
        buck_path = S3_targ_splt[2]
        key_path = '/'.join(S3_targ_splt[3:])

        # Load model
        s3 = ial.get_s3_resource()
        datos = s3.meta.client.get_object(Bucket = buck_path, Key = key_path)
        body = datos['Body'].read()
        df_model = pkl.loads(body)

        print("\n\n ======= ======= =======   DOWNLOAD MODEL   ======= ======= ======= \n\n", type(df_model))

        
    # ^ Import FE dataset from RDS db.
        conn = psycopg2.connect(dbname = self.input()['A'].database, user = self.input()['A'].user, password = self.input()['A'].password,
                                port = self.input()['A'].port, host = self.input()['A'].host)
        
        str_qry = "SELECT * FROM procdata.feat_eng WHERE ingest_date between '" + str_date + "' and '" + str_date + "';"
        df_fe_to_pred = sqlio.read_sql_query(str_qry, conn)

                
    # > Predictions.
        df_predicts = predict(df_fe_to_pred, df_model)
        
        print("\n\n ======= ======= =======   NEW PREDICTIONS   ======= ======= ======= \n\n\t", type(df_predicts),
              "\n\n", df_predicts.head(3), "\n\n")
    
        with self.output().open('w') as f:
            pkl.dump(df_predicts, f)
                    
    # > Lineage. Creating Metadata @ .csv file
        
      # > Set path to S3   
    
        str_file = "newpredicts-" + str_date + ".pkl"
        path_S3 = "s3://{}/newpredicts/YEAR={}/MONTH={}/DAY={}/{}".\
        format(self.bucket, self.year, self.month, self.day, str_file)        
        
      # > Lineage. Creating Metadata @ .csv file       
        str_file_csv = str_date + ".csv"
        output_path = "src/temp/metadata/newpredicts/type={}/".format(self.flg_i0_c1)
        os.makedirs(output_path, exist_ok = True)
        
        dic_par = {'year':str(self.year),'month':str(self.month),'day':str(self.day),'flg_i0_c1':str(self.flg_i0_c1)}
        df = pd.DataFrame({'exec_date': [self.todate], 'exec_param': [json.dumps(dic_par)],'executer': ['luigi'],
                           'num_new_preds': [df_predicts.shape[0]], 'S3_store_path': [path_S3]})
        df.to_csv(output_path + str_file_csv, index=False, header=False)
                
    def output(self):
    # 0 Formatting date parameters into date-string
        str_date = str(datetime.date(datetime(self.year, self.month, self.day)))

    # 0 Set path to S3
        str_file = "newpredicts-" + str_date + ".pkl"
        output_path = "s3://{}/newpredicts/YEAR={}/MONTH={}/DAY={}/{}".\
        format(self.bucket, self.year, self.month, self.day, str_file)
        
        s3 = ial.get_luigi_s3client()
        return luigi.contrib.s3.S3Target(path = output_path, client = s3, format = luigi.format.Nop)
