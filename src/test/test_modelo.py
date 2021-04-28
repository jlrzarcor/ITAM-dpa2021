# ================================= LIBRARIES  ================================= #

# importing packages
import pandas as pd
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

# ================================= FUNCTION: testing DF ================================= #

class TestModel(marbles.core.TestCase):
    
    # Variables
    todate = datetime.date(datetime.today())
    test_meth = ''
    status = ''
    err_msg = ''

    __name__ = 'TestModel'
    
    def test_score(self):

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
        A = str(type(model_cfi))
        comp_val = ""
        if pd.read_csv('src/test/trans_file.csv', header = None).iloc[0,1] == 1:
            comp_val = "<class 'sklearn.tree._classes.DecisionTreeClassifier'>"

        self.assertEqual(A, comp_val, note = "^^^^^^^^   El mejor modelo seleccionado no coincide con <class 'sklearn.tree._classes.DecisionTreeClassifier'>.    ^^^^^^^^\n")
        self.status = "TestPassed:)"
        self.test_meth = "test_score"