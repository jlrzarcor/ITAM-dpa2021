# ================================= LIBRARIES  ================================= #

# importing packages
import pandas as pd
import numpy as np
import marbles.core
import pickle
import json
import boto3
from datetime import datetime
import os

# importing especific functions
from luigi.contrib.s3 import S3Target
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.tree import DecisionTreeClassifier

# importing custom libraries
import src.utils.constants as ks
from src.utils.general import get_pg_service
import src.pipeline.ingesta_almacenamiento as ial

# Requires...

# ================================= FUNCTION: testing Scores ================================= #

class TestPredict(marbles.core.TestCase):
    
    # Variables
    todate = datetime.date(datetime.today())
    test_meth = ''
    status = ''
    err_msg = ''

    __name__ = 'TestPredict'
    
    def test_avg_prec(self):

        S3_targ = pd.read_csv('src/test/trans_file.csv', header = None).iloc[0,0]
        
        # Path from S3 client to open data @ S3
        S3_targ_splt = S3_targ.split("/")
        buck_path = S3_targ_splt[2]
        key_path = '/'.join(S3_targ_splt[3:])

        # Create a DataFrame from S3 data
        s3 = ial.get_s3_resource()
        datos = s3.meta.client.get_object(Bucket = buck_path, Key = key_path)
        body = datos['Body'].read()
        model_cfi = pickle.loads(body)
        avg_prec = model_cfi['score'].mean()
        
        req_prec = float(pd.read_csv('src/test/trans_file.csv', header = None).iloc[0,1])/100
        
        self.assertGreater(avg_prec, req_prec , note = "\n\n ======= ======= =======   Los scores de las nuevas predicciones está por debajo de la precisión indicada, Mario... parece que se nos desconecto el pipeline powpow.   ======= ======= ======= \n\n")
        self.status = "TestPassed:)"
        self.test_meth = "test_avg_prec"