# ================================= LIBRARIES  ================================= #

import luigi
import luigi.contrib.s3
import boto3
import os
import json
import pickle as pkl

from sodapy import Socrata
from datetime import datetime


# Variables de entorno que se cargan por default al cargar la librería
# ingesta_almacenamiento.py

# importing custom libraries
import src.utils.general as gral
import src.utils.constants as ks
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
        str_date = datetime.date(datetime(self.year,self.month,self.day))
        
    # SODAPY. Connecting client to Socrata and Ingestion -> json.dumps
        client = ial.get_client()
            # Debug print: print("Raise Flag Success:", client)

        if self.flg_i0_c1 == 0:
            data_i = ial.ingesta_inicial(client, str_date + 'T00:00:00.000', 300)
        else:
            data_i = ial.ingesta_consecutiva(client, str_date + 'T00:00:00.000', 3)
        
        json_data = json.dumps(data_i, indent=4)
        
            # Debug print: print("Raise Flag", data_i, "X-Man", ks.path, "json", json_data)
    # Call output
        with self.output().open('w') as output_file:
            output_file.write(json_data)
        
    def output(self):    
        output_path = "./src/temp/TYPINGST={}/ingesta.json".format(self.flg_i0_c1)
        return luigi.local_target.LocalTarget(path=output_path)