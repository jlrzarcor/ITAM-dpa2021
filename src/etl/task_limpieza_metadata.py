# ================================= LIBRARIES  ================================= #

# importing packages
import luigi
import json
import pandas as pd
import psycopg2
import yaml

# importing especific functions
from luigi.contrib.postgres import CopyToTable
from datetime import datetime

# importing custom libraries
import src.utils.constants as ks
from src.utils.general import get_pg_service

# Requires...
from src.etl.task_limpieza_unit_test import TaskCleaningUnitTest

### ---->>> Review in all pipeline remove unnecesary
#from src.etl.task_ingestion_metadata import TaskIngestMeta
#from src.etl.task_almacenamiento import TaskStore



# ================================= LUIGI TASK ================================= #

class TaskCleaningMeta(CopyToTable):
    
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
        return TaskCleaningUnitTest(self.bucket, self.prc_path, self.year, self.month, self.day, self.flg_i0_c1)


    # RDS database connection
    pg = get_pg_service(ks.path)
    user = pg['user']
    password = pg['password']
    host = pg['host']
    port = pg['port']
    database = pg['dbname']
    table = 'metadata.cleaning'

    
    # RDS database table columns
    columns = [("exec_date", "date"), ("exec_param", "json"), ("executer", "varchar"), ("source_path", "text"), ("nrows_prev", "int"),
               ("ncols_prev", "int"), ("nrows_after", "int"), ("ncols_after", "int"), ("nulls", "int")]
    

    def rows(self):
        str_file = str(datetime.date(datetime(self.year, self.month, self.day))) + ".csv"
        output_path = "src/temp/metadata/limpieza/type={}/".format(self.flg_i0_c1)
        data = pd.read_csv(output_path + str_file, header = None)
        for row in data.itertuples(index = False):
            yield row



