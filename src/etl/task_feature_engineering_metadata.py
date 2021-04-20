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
from src.etl.task_feature_engineering import TaskFeatEng


# ================================= LUIGI TASK ================================= #

class  TaskFeatEngMeta(CopyToTable):

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
        return  TaskFeatEng(self.bucket, self.prc_path, self.year, self.month, self.day, self.flg_i0_c1)

    # RDS database connection
    pg = get_pg_service(ks.path)
    user = pg['user']
    password = pg['password']
    host = pg['host']
    port = pg['port']
    database = pg['dbname']
    table = 'metadata.feat_eng'

    # RDS database table columns
    columns = [("exec_date","date"), ("exec_param","json"), ("executer","varchar"), ("source_path","text"), ("nrow_ohe","int"),
               ("ncols_ohe","int"), ("best_score","real"), ("time_exec","real"), ("best_rf","text")]

    def rows(self):
        str_file = str(datetime.date(datetime(self.year, self.month, self.day))) + ".csv"
        output_path = "src/temp/metadata/fe/type={}/".format(self.flg_i0_c1)
        data = pd.read_csv(output_path + str_file, header = None)
        for row in data.itertuples(index = False):
            yield row
