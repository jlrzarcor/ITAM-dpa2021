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
import src.test.test_ingestion as tsi

# Requires...
from src.etl.task_ingesta import TaskIngest

# ================================= LUIGI TASK ================================= #

class TaskIngestUnitTest(CopyToTable):
    
    # Variables
      # Transfer required variables    
        
    todate = datetime.date(datetime.today())
    year = luigi.IntParameter(default = todate.year)
    month = luigi.IntParameter(default = todate.month)
    day = luigi.IntParameter(default = todate.day)
    
    flg_i0_c1 = luigi.IntParameter(default = 1)

    def requires(self):
        return TaskIngest(self.year, self.month, self.day, self.flg_i0_c1)    
    
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
        marble_obj = tsi.TestIngest()
        marble_obj.test_df_not_empty()
        
        os.system('rm src/test/trans_file.csv')
        
        # unit-test pass report metadata into tupple        
        dic_par = {'year':str(self.year),'month':str(self.month),'day':str(self.day),'flg_i0_c1':str(self.flg_i0_c1)}
        df = pd.DataFrame({'test_meth': [marble_obj.test_meth], 'test_stat': [marble_obj.status], 'test_msg': [marble_obj.err_msg],
                           'exec_date': [self.todate], 'exec_param': [json.dumps(dic_par)],'executer': ['luigi']
                          })
    
        for row in df.itertuples(index = False):
            yield row
