# ================================= LIBRARIES  ================================= #

import luigi
import luigi.contrib.s3
import json

import boto3
import pickle as pkl
from sodapy import Socrata
from datetime import datetime

import src.utils.constants as ks
from src.utils.general import get_api_token, get_s3_credentials
from task_ingesta import TaskIngest

# Variables de entorno que se cargan por default al cargar la librería
# ingesta_almacenamiento.py

# importing libraries required.

import pandas as pd
import numpy as np

# importing custom libraries
import src.utils.general as gral
import src.utils.constants as ks
import src.pipeline.ingesta_almacenamiento as ial


# ================================= LUIGI TASK  ================================= #


class TaskStore(luigi.Task):
    
#    bucket = luigi.Parameter(default = "data-product-architecture-equipo-5")
    
    bucket = luigi.Parameter(default = "temp-dev-dpa")
    prc_path = luigi.Parameter(default = "ingestion")
    
    todate = datetime.date(datetime.today())
    year = luigi.IntParameter(default = todate.year)
    month = luigi.IntParameter(default = todate.month)
    day = luigi.IntParameter(default = todate.day)
    
    flg_i0_c1 = luigi.IntParameter(default = 1)

    def requires(self):
        return {'a' : TaskIngest(self.flg_i0_c1, self.year, self.month, self.day)}
    
    def run(self):
        fecha = (datetime.date(datetime.now()))
        anio = (datetime.year(datetime.now()))
        mes = (datetime.mont(datetime.now()))
        print("==============>>>> Fechas", fecha, anio, mes)
        s3 = ial.get_s3_resource()
        data = json.load(self.input()['a'].open('r'))

        with self.output().open('w') as f:
            pkl.dump(data, f)
                    
        
    def output(self):
        
        if self.flg_i0_c1 == 0:
            flag = "initial"
            + "historic-inspections-" + fecha + ".pckl"
            
            output_path = "s3://{}/{}/{}/YEAR={}/MONTH={}/historic-inspections.pckl".\
            format(self.bucket, self.path_i, flag, self.year, str(self.month))           
        else:
            bucket_path = "consecutive"
            + "consecutive-inspections-" + fecha + ".pckl"
            
            output_path = "s3://{}/{}/{}/YEAR={}/MONTH={}/historic-inspections.pckl".\
            format(self.bucket, self.prc_path, flag, self.year, str(self.month))


        
        return luigi.contrib.s3.S3Target(path = output_path, format = luigi.format.Nop)