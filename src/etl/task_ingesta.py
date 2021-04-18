# ================================= LIBRARIES  ================================= #

# importing packages
import luigi
import pandas as pd
import json
from datetime import datetime
import os

# importing custom libraries
import src.pipeline.ingesta_almacenamiento as ial


# ================================= LUIGI TASK ================================= #


class TaskIngest(luigi.Task):
    
    todate = datetime.date(datetime.today())
    year = luigi.IntParameter(default = todate.year)
    month = luigi.IntParameter(default = todate.month)
    day = luigi.IntParameter(default = todate.day)
    
    flg_i0_c1 = luigi.IntParameter(default = 1)
        
    def run(self):
    # Formatting date parameters into date-string
        str_date = str(datetime.date(datetime(self.year, self.month, self.day)))
        
    # SODAPY. Connecting client to Socrata and Ingestion -> json.dumps
        client = ial.get_client()

        if self.flg_i0_c1 == 0:
            data_i = ial.ingesta_inicial(client, delta_date = str_date + 'T00:00:00.000', limit = 300000)
        else:
            data_i = ial.ingesta_consecutiva(client, delta_date = str_date + 'T00:00:00.000', limit = 1000)

        json_data = json.dumps(data_i, indent=4)            
            
    # Lineage. Creating Metadata @ .csv file
        str_file = str_date + ".csv"
        output_path = "src/temp/metadata/ingestion/type={}/".format(self.flg_i0_c1)
        os.makedirs(output_path, exist_ok = True)
        
        dic_par = {'year':str(self.year),'month':str(self.month),'day':str(self.day),'flg_i0_c1':str(self.flg_i0_c1)}
        df = pd.DataFrame({'fecha': [str_date], 'param_exec': [json.dumps(dic_par)],'usuario': ['luigi'], 'num_regs_ing': [len(data_i)]})
        df.to_csv(output_path + str_file, index=False, header=False)
        
    # Call output
        with self.output().open('w') as output_file:
            output_file.write(json_data)
        
    def output(self):
        str_file = "ingesta" + str(datetime.date(datetime(self.year,self.month,self.day))) + ".json"
        output_path = "./src/temp/TYPINGST={}/{}".format(self.flg_i0_c1, str_file)
        return luigi.local_target.LocalTarget(path=output_path)