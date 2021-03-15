# ================================= LIBRARIES  ================================= #

# importing packages
import luigi
import json
from datetime import datetime

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
        str_date = str(datetime.date(datetime(self.year, self.month, self.day))) + 'T00:00:00.000'
        
    # SODAPY. Connecting client to Socrata and Ingestion -> json.dumps
        client = ial.get_client()

        if self.flg_i0_c1 == 0:
            data_i = ial.ingesta_inicial(client, delta_date = str_date , limit = 300)
        else:
            data_i = ial.ingesta_consecutiva(client, delta_date = str_date, limit = 3)
        
        json_data = json.dumps(data_i, indent=4)
        
    # Call output
        with self.output().open('w') as output_file:
            output_file.write(json_data)
        
    def output(self):
        str_file = "ingesta" + str(datetime.date(datetime(self.year,self.month,self.day))) + ".json"
        output_path = "./src/temp/TYPINGST={}/{}".format(self.flg_i0_c1, str_file)
        return luigi.local_target.LocalTarget(path=output_path)