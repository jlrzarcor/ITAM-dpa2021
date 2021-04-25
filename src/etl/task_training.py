# importing packages
import luigi
import json
import pandas as pd
import psycopg2
import yaml
import os
import pandas.io.sql as sqlio

# importing especific functions
from luigi.contrib.postgres import CopyToTable
from datetime import datetime

# importing custom libraries
import src.utils.constants as ks
from src.utils.general import get_pg_service

# Requires...
from src.etl.task_feature_engineering import TaskFeatEng
from src.etl.task_feature_engineering_metadata import TaskFeatEngMeta
from src.utils.training import train

# ================================= LUIGI TASK ================================= #


class TaskTrain(luigi.Task):
class TaskTrain(CopyToTable):
    
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
    
    # RDS database connection
    pg = get_pg_service(ks.path)
    user = pg['user']
    password = pg['password']
    host = pg['host']
    port = pg['port']
    database = pg['dbname']
    #table = 'procdata.feat_eng'

    # RDS database table columns
    #columns = [("label_risk", "int"), ("label_results", "int"), ("zip", "varchar"), ("facility_type", "text")]
    
    def rows(self):
        
      # Create a DataFrame from clean data from RDS db.
        pg_aux = get_pg_service(ks.path)
        conn = psycopg2.connect(dbname = pg_aux['dbname'], user = pg_aux['user'], password = pg_aux['password'],
                                port = pg_aux['port'], host = pg_aux['host'])
        str_qry = "SELECT * FROM procdata.feat_eng;"
        feature_eng = sqlio.read_sql_query(str_qry, conn)
        
      # Apply Training to data.
        X_train, y_train, X_test, y_test, nrows_ohe, ncols_ohe = train(feature_eng)
        
        print("\n\n++++++++++++++++++ FEATURE ENGINEERING ++++++++++++++++++\n\n",
              type(X_train), type(y_train), type(X_test), type(y_test), nrows_train, ncols_train)
        
      # Lineage. Creating Metadata @ .csv file
        str_date = str(datetime.date(datetime(self.year, self.month, self.day)))
           
        str_file_csv = str_date + ".csv"
        output_path = "src/temp/metadata/fe/type={}/".format(self.flg_i0_c1)
        os.makedirs(output_path, exist_ok = True)
        
        dic_par = {'year':str(self.year),'month':str(self.month),'day':str(self.day),'flg_i0_c1':str(self.flg_i0_c1)}
        
        df = pd.DataFrame({'nrows_train': [nrows_train], 'ncols_train': [ncols_train]})
        
        df.to_csv(output_path + str_file_csv, index=False, header=False)
        
# ----------------------------------------------------------------------------
        
    # Load data into RDS procdata.feat_eng
        for row in feat_eng_df.itertuples(index = False):
            yield row

# ----------------------------------------------------------------------------
    def output(self):
    # Formatting date parameters into date-string
        str_date = str(datetime.date(datetime(self.year, self.month, self.day)))

    # Set path to S3   
        if self.flg_i0_c1 == 0:
            flag = "initial"
            str_file = "historic-inspections-" + str_date + ".pkl"
            output_path = "s3://{}/{}/{}/YEAR={}/MONTH={}/DAY={}/{}".\
            format(self.bucket, self.prc_path, flag, self.year, self.month, self.day, str_file)
            
        else:
            flag = "consecutive"
            str_file = "consecutive-inspections-" + str_date + ".pkl"
            output_path = "s3://{}/{}/{}/YEAR={}/MONTH={}/DAY={}/{}".\
            format(self.bucket, self.prc_path, flag, self.year, self.month, self.day, str_file)
            
        s3 = ial.get_luigi_s3client()
        return luigi.contrib.s3.S3Target(path = output_path, client = s3, format = luigi.format.Nop)  