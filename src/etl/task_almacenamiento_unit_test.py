# ================================= LIBRARIES  ================================= #

# importing packages
import luigi
import json
#import boto3
import pandas as pd
import psycopg2
import yaml
import os
import pandas.io.sql as sqlio

# importing especific functions
from luigi.contrib.postgres import CopyToTable
#from luigi.contrib.s3 import S3Target
from datetime import datetime

# importing custom libraries
import src.utils.constants as ks
from src.utils.general import get_pg_service
import src.test.test_almacenamiento as tsa

# Requires...
from src.etl.task_almacenamiento import TaskStore

# ================================= LUIGI TASK ================================= #

class TaskStoreUnitTest(CopyToTable):
    
    # Variables
      # Transfer required variables    
    bucket = luigi.Parameter(default = "data-product-architecture-equipo-5")
    prc_path = luigi.Parameter(default = "ingestion")
        
    todate = datetime.date(datetime.today())
    year = luigi.IntParameter(default = todate.year)
    month = luigi.IntParameter(default = todate.month)
    day = luigi.IntParameter(default = todate.day)
    
    flg_i0_c1 = luigi.IntParameter(default = 1)

    def requires(self):
        return TaskStore(self.bucket, self.prc_path, self.year, self.month, self.day, self.flg_i0_c1)
    
    # RDS database connection
    pg = get_pg_service(ks.path)
    user = pg['user']
    password = pg['password']
    host = pg['host']
    port = pg['port']
    database = pg['dbname']
    table = 'metadata.unittest'

    # RDS database table columns
    columns = [("test_meth", "varchar"), ("test_stat", "varchar"), ("test_msg", "varchar"),
               ("exec_date", "date"), ("exec_param", "json"), ("executer", "varchar")]
        
    def rows(self):

        # Create a transfer file path to target unit test...
        os.system('echo ' + self.input().path + ' > src/test/trans_file.csv')

        # Objects returned by test
        marble_obj = tsa.TestStoredS3()
        marble_obj.test_num_col()
        
        os.system('rm src/test/trans_file.csv')
        
        # unit-test pass report metadata into tupple        
        dic_par = {'year':str(self.year),'month':str(self.month),'day':str(self.day),'flg_i0_c1':str(self.flg_i0_c1),
                   'aws_s3_path':str(self.input().path)}
        df = pd.DataFrame({'test_meth': [marble_obj.test_meth], 'test_stat': [marble_obj.status], 'test_msg': [marble_obj.err_msg],
                           'exec_date': [self.todate], 'exec_param': [json.dumps(dic_par)],'executer': ['luigi']
                          })
    
        for row in df.itertuples(index = False):
            yield row
