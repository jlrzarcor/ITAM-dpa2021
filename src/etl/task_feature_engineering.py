# ================================= LIBRARIES  ================================= #

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
from src.etl.task_limpieza import TaskCleaning
from src.etl.task_limpieza_metadata import TaskCleaningMeta
from src.utils.feature_engineering import feat_eng

# ================================= LUIGI TASK ================================= #


class TaskFeatEng(CopyToTable):
    
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
        return {'A':TaskCleaning(self.bucket, self.prc_path, self.year, self.month, self.day, self.flg_i0_c1),
                'B':TaskCleaningMeta(self.bucket, self.prc_path, self.year, self.month, self.day, self.flg_i0_c1)}
    
 # RDS database connection for CopyToTable
    pg = get_pg_service(ks.path)
    user = pg['user']
    password = pg['password']
    host = pg['host']
    port = pg['port']
    database = pg['dbname']
    table = 'procdata.feat_eng'

 # RDS database table columns for CopyToTable
    columns = [("ingest_date", "date"),("aka_name", "varchar"), ("license", "varchar"), ("label_risk", "int"),
               ("label_results", "int"), ("level", "varchar"), ("class", "text")]
    
    def rows(self):

        str_date = str(datetime.date(datetime(self.year, self.month, self.day)))        
        
     # Create a DataFrame from clean data from RDS db.
        pg_aux = get_pg_service(ks.path)
        conn = psycopg2.connect(dbname = pg_aux['dbname'], user = pg_aux['user'], password = pg_aux['password'],
                                port = pg_aux['port'], host = pg_aux['host'])

        str_qry = "SELECT * FROM procdata.limpieza WHERE ingest_date between '" + str_date + "' and '" + str_date + "';"
        clean_data = sqlio.read_sql_query(str_qry, conn)
        clean_data.drop(columns = 'ingest_date', inplace=True, errors='raise')
        
     # Apply FE to data.
        feat_eng_df, nrows_ohe, ncols_ohe, best_score, time_exec, best_rf = feat_eng(clean_data)
        feat_eng_df.insert(0, "ingest_date", datetime.date(datetime(self.year, self.month, self.day)))
        
        print("\n\n ======= ======= =======   FEATURE ENGINEERING   ======= ======= =======\n\n")
        
     # Lineage. Creating Metadata @ .csv file
           
        str_file_csv = str_date + ".csv"
        output_path = "src/temp/metadata/fe/type={}/".format(self.flg_i0_c1)
        os.makedirs(output_path, exist_ok = True)
        
        dic_par = {'year':str(self.year),'month':str(self.month),'day':str(self.day),'flg_i0_c1':str(self.flg_i0_c1)}
        
        df = pd.DataFrame({'exec_date': [self.todate], 'exec_param': [json.dumps(dic_par)],'executer': ['luigi'],
                           'source_path': [pg_aux['host']], 'nrows_ohe': [nrows_ohe], 'ncols_ohe': [ncols_ohe],
                           'best_score': [best_score], 'time_exec': [time_exec], 'best_rf': [best_rf]})
        
        df.to_csv(output_path + str_file_csv, index=False, header=False)
        
     # Load data into RDS procdata.feat_eng
        for row in feat_eng_df.itertuples(index = False):
            yield row




