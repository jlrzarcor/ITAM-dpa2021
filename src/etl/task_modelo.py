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
from src.etl.task_training import TaskTrain
from src.etl.task_training_metadata import TaskTrainMeta
from src.utils.model import model

# ================================= LUIGI TASK ================================= #


class TaskModel(luigi.Task):
    
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
    
    force3_err = luigi.IntParameter(default = 1)
    
    def requires(self):
        return {'A':TaskTrain(self.bucket, self.prc_path, self.year, self.month, self.day, self.flg_i0_c1),
                'B':TaskTrainMeta(self.bucket, self.prc_path, self.year, self.month, self.day, self.flg_i0_c1, self.force3_err)}    
    
    def run(self):
        
        # Path from S3 client to open data @ S3
        S3_targ = self.input()['A'].path
        S3_targ_splt = S3_targ.split("/")
        buck_path = S3_targ_splt[2]
        key_path = '/'.join(S3_targ_splt[3:])

        # Create a DataFrame from S3 data
        s3 = ial.get_s3_resource()
        datos = s3.meta.client.get_object(Bucket = buck_path, Key = key_path)
        body = datos['Body'].read()
        df_trained = pkl.loads(body)
        
    # Apply Training to data.
        obj_model, best_tree, t_exec, test_models, mean_scores, rank_model = model(df_trained)
        
        print("\n\n++++++++++++++++++ MODELING ++++++++++++++++++\n\n", type(obj_model), type(best_tree))
    
        with self.output().open('w') as f:
            pkl.dump(obj_model, f)
                    
    # Lineage. Creating Metadata @ .csv file
        str_date = str(datetime.date(datetime(self.year, self.month, self.day)))

    # Set path to S3   
        str_file = "modelo-" + str_date + ".pkl"
        path_S3 = "s3://{}/modelo/YEAR={}/MONTH={}/DAY={}/{}".\
        format(self.bucket, self.year, self.month, self.day, str_file)        
        
      # Lineage. Creating Metadata @ .csv file
        str_date = str(datetime.date(datetime(self.year, self.month, self.day)))
           
        str_file_csv = str_date + ".csv"
        output_path = "src/temp/metadata/modelo/type={}/".format(self.flg_i0_c1)
        os.makedirs(output_path, exist_ok = True)
        
        dic_par = {'year':str(self.year),'month':str(self.month),'day':str(self.day),'flg_i0_c1':str(self.flg_i0_c1)}
        df = pd.DataFrame({'exec_date': [self.todate], 'exec_param': [json.dumps(dic_par)],'executer': ['luigi'],
                           'best_tree': [best_tree], 'exec_time': [t_exec], 'test_models': [test_models], 'score': [mean_scores],
                            'rank': [rank_model]}) #, 'S3_path': [path_S3]})
        df.to_csv(output_path + str_file_csv, index=False, header=False)
                
    def output(self):
    # Formatting date parameters into date-string
        str_date = str(datetime.date(datetime(self.year, self.month, self.day)))

    # Set path to S3   
        str_file = "modelo-" + str_date + ".pkl"
        output_path = "s3://{}/modelo/YEAR={}/MONTH={}/DAY={}/{}".\
        format(self.bucket, self.year, self.month, self.day, str_file)
            
        s3 = ial.get_luigi_s3client()
        return luigi.contrib.s3.S3Target(path = output_path, client = s3, format = luigi.format.Nop)  
    