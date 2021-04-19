# ================================= LIBRARIES  ================================= #

# importing libraries required.
import luigi
import luigi.contrib.s3
import json
import os
import pickle as pkl
import pandas as pd
from datetime import datetime

# importing custom libraries and modules
from src.etl.task_ingesta import TaskIngest
from src.etl.task_ingestion_metadata import TaskIngestMeta
import src.pipeline.ingesta_almacenamiento as ial


# ================================= LUIGI TASK  ================================= #


class TaskStore(luigi.Task):
    
    bucket = luigi.Parameter(default = "data-product-architecture-equipo-5")
#    bucket = luigi.Parameter(default = "temp-dev-dpa")
    prc_path = luigi.Parameter(default = "ingestion")
    
    todate = datetime.date(datetime.today())
    year = luigi.IntParameter(default = todate.year)
    month = luigi.IntParameter(default = todate.month)
    day = luigi.IntParameter(default = todate.day)
    
    flg_i0_c1 = luigi.IntParameter(default = 1)
    
    def requires(self):
        return {'a' : TaskIngest(self.year, self.month, self.day, self.flg_i0_c1),
                'b' : TaskIngestMeta(self.year, self.month, self.day, self.flg_i0_c1)}
    
    def run(self):
        data = json.load(self.input()['a'].open('r'))

        with self.output().open('w') as f:
            pkl.dump(data, f)
                    
    # Lineage. Creating Metadata @ .csv file
        str_date = str(datetime.date(datetime(self.year, self.month, self.day)))
        
        if self.flg_i0_c1 == 0:
            flag = "initial"
            str_file = "historic-inspections-" + str_date + ".pkl"
            path_S3 = "s3://{}/{}/{}/YEAR={}/MONTH={}/DAY={}/{}".\
            format(self.bucket, self.prc_path, flag, self.year, self.month, self.day, str_file)
            
        else:
            flag = "consecutive"
            str_file = "consecutive-inspections-" + str_date + ".pkl"
            path_S3 = "s3://{}/{}/{}/YEAR={}/MONTH={}/DAY={}/{}".\
            format(self.bucket, self.prc_path, flag, self.year, self.month, self.day, str_file)
    
    
        str_file_csv = str_date + ".csv"
        output_path = "src/temp/metadata/almacenamiento/type={}/".format(self.flg_i0_c1)
        os.makedirs(output_path, exist_ok = True)
        
        dic_par = {'year':str(self.year),'month':str(self.month),'day':str(self.day),'flg_i0_c1':str(self.flg_i0_c1)}
        df = pd.DataFrame({'fecha': [self.todate], 'param_exec': [json.dumps(dic_par)],'usuario': ['luigi'],
                           'num_regs_almac': [len(data)], 'ruta_S3': [path_S3]})
        df.to_csv(output_path + str_file_csv, index=False, header=False)
                
                
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
