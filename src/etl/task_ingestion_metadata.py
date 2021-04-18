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
from src.utils.general2 import get_pg_service

# Requires...
from src.etl.task_ingesta import TaskIngest


# ================================= LUIGI TASK ================================= #

class TaskIngestMeta(CopyToTable):
    
    # Variables
    todate = datetime.date(datetime.today())
    
    year = luigi.IntParameter(default = todate.year)
    month = luigi.IntParameter(default = todate.month)
    day = luigi.IntParameter(default = todate.day)
    
    flg_i0_c1 = luigi.IntParameter(default = 1)
    
    def requires(self):
        #return {'a' : TaskIngest(self.year, self.month, self.day, self.flg_i0_c1)}
        return TaskIngest(self.year, self.month, self.day, self.flg_i0_c1)

    # RDS database connection
    pg = get_pg_service(ks.path)
    user = pg['user']
    password = pg['password']
    host = pg['host']
    port = pg['port']
    database = pg['dbname']
    table = 'metadata.ingestion'

    # RDS database table columns
    columns = [("fecha", "date"), ("param_exec", "json"), ("usuario", "varchar"), ("num_regs_ing", "int")]

    def rows(self):
        # Rememeber, we must use tupples
        str_file = str(datetime.date(datetime(self.year, self.month, self.day))) + ".csv"
        output_path = "src/temp/metadata/ingestion/type={}/".format(self.flg_i0_c1)
        data = pd.read_csv(output_path + str_file, header = None)
        
        for row in data.itertuples(index = False):
            yield row