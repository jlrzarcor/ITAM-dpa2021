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
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.tree import DecisionTreeClassifier
from datetime import datetime

# importing custom libraries
import src.utils.constants as ks
from src.utils.general import get_pg_service
import src.pipeline.ingesta_almacenamiento as ial

# Requires...
from src.etl.task_modelo import TaskModel
from src.etl.task_modelo_metadata import TaskModelMeta
from src.etl.task_training import TaskTrain
from src.etl.task_feature_engineering import TaskFeatEng
from src.utils.bias_fairness import bias_fair


# ================================= LUIGI TASK ================================= #


class TaskBiasFair(luigi.Task):
    
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
    
    force4_err = luigi.IntParameter(default = 1)
    
    def requires(self):
        return {'A':TaskModel(self.bucket, self.prc_path, self.year, self.month, self.day, self.flg_i0_c1),
                'B':TaskModelMeta(self.bucket, self.prc_path, self.year, self.month, self.day, self.flg_i0_c1, self.force4_err),
                'C':TaskTrain(self.bucket, self.prc_path, self.year, self.month, self.day, self.flg_i0_c1),
                'D':TaskFeatEng(self.bucket, self.prc_path, self.year, self.month, self.day, self.flg_i0_c1)
               }
    
    def run(self):
        
    # Import Selected Model from AWS-S3
        # Path for S3 client to open data @ S3
        S3_targ = self.input()['A'].path
        S3_targ_splt = S3_targ.split("/")
        buck_path = S3_targ_splt[2]
        key_path = '/'.join(S3_targ_splt[3:])

        # Load model
        s3 = ial.get_s3_resource()
        datos = s3.meta.client.get_object(Bucket = buck_path, Key = key_path)
        body = datos['Body'].read()
        df_model = pkl.loads(body)

    # Import Train-Test Dataset from AWS-S3
        # Path for S3 client to open data @ S3
        S3_targ_tt = self.input()['C'].path
        S3_targ_splt_tt = S3_targ_tt.split("/")
        buck_path_tt = S3_targ_splt_tt[2]
        key_path_tt = '/'.join(S3_targ_splt_tt[3:])

        # Load data
        s3_tt = ial.get_s3_resource()
        datos_tt = s3_tt.meta.client.get_object(Bucket = buck_path, Key = key_path_tt)
        body_tt = datos_tt['Body'].read()
        df_tt = pkl.loads(body_tt)
        
    # Import FE dataset from RDS db.
        conn = psycopg2.connect(dbname = self.input()['D'].database, user = self.input()['D'].user, password = self.input()['D'].password,
                                port = self.input()['D'].port, host = self.input()['D'].host)
        
        str_qry = "SELECT * FROM procdata.feat_eng;"
        df_fe = sqlio.read_sql_query(str_qry, conn)
        
                
    # Apply Bias&Fairness.
        df_labels, metrics_to_rds, n_grps, n_atrib, ppp, ppr = bias_fair(df_model, df_tt, df_fe)
        
        print("\n\n +++++++ BIAS AND FAIRNESS ++++++++ \n\n")
    
        with self.output().open('w') as f:
            pkl.dump(metrics_to_rds, f)
                    
    # Lineage. Creating Metadata @ .csv file
        str_date = str(datetime.date(datetime(self.year, self.month, self.day)))
        
    # Set path to S3   
        str_file = "modelo-" + str_date + ".pkl"
        path_S3 = "s3://{}/biasandfair/YEAR={}/MONTH={}/DAY={}/{}".\
        format(self.bucket, self.year, self.month, self.day, str_file)        
        
    # Lineage. Creating Metadata @ .csv file
        str_date = str(datetime.date(datetime(self.year, self.month, self.day)))
           
        str_file_csv = str_date + ".csv"
        output_path = "src/temp/metadata/biasandfair/type={}/".format(self.flg_i0_c1)
        os.makedirs(output_path, exist_ok = True)
        
        dic_par = {'year':str(self.year),'month':str(self.month),'day':str(self.day),'flg_i0_c1':str(self.flg_i0_c1)}
        df = pd.DataFrame({'exec_date': [self.todate], 'exec_param': [json.dumps(dic_par)],'executer': ['luigi'],
                           'num_regs': [df_labels.shape[0]], 'num_grps': [n_grps], 'num_atrib': [n_atrib],
                           'prop_pos_pred': [ppp], 'prop_pos_real': [ppr], 'S3_store_path': [path_S3]})
        df.to_csv(output_path + str_file_csv, index=False, header=False)
                
    def output(self):
    # Formatting date parameters into date-string
        str_date = str(datetime.date(datetime(self.year, self.month, self.day)))

    # Set path to S3
        str_file = "biasandfair-" + str_date + ".pkl"
        output_path = "s3://{}/biasandfair/YEAR={}/MONTH={}/DAY={}/{}".\
        format(self.bucket, self.year, self.month, self.day, str_file)
        
        s3 = ial.get_luigi_s3client()
        return luigi.contrib.s3.S3Target(path = output_path, client = s3, format = luigi.format.Nop)
