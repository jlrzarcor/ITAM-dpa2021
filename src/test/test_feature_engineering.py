# ================================= LIBRARIES  ================================= #

# importing packages
import pandas as pd
import marbles.core
import psycopg2
import pandas.io.sql as sqlio
from datetime import datetime
import os

# importing especific functions

# importing custom libraries
import src.utils.constants as ks
from src.utils.general import get_pg_service
import src.pipeline.ingesta_almacenamiento as ial

# Requires...

# ================================= FUNCTION: testing DF ================================= #

class TestFeatEng(marbles.core.TestCase):
    
    # Variables
    todate = datetime.date(datetime.today())
    test_meth = ''
    status = ''
    err_msg = ''

    __name__ = 'TestFeatEng'
    
    def test_integrity(self):

        RDS_targ = pd.read_csv('src/test/trans_file.csv', header = None)
        
      # Create a DataFrame from clean data from RDS db.
        conn = psycopg2.connect(dbname = RDS_targ.iloc[0,0], user = RDS_targ.iloc[0,2], password = RDS_targ.iloc[0,3],
                                port = RDS_targ.iloc[0,4], host = RDS_targ.iloc[0,5])
        #dbtable = RDS_targ.iloc[0,1],
        str_qry1 = "SELECT DISTINCT(label_risk) AS risk_levels FROM procdata.feat_eng;"
        clean_data1 = sqlio.read_sql_query(str_qry1, conn)
        str_qry2 = "SELECT DISTINCT(label_results) AS y_levels FROM procdata.feat_eng;"
        clean_data2 = sqlio.read_sql_query(str_qry2, conn)
        
        list_tst = [clean_data1.shape[0], clean_data2.shape[0] ]
        list_cmpr = [3, 2]
        
        self.assertListEqual(list_tst, list_cmpr , note = "^^^^^^^^   Los valores únicos para la variable respuesta son (0, 1) y para la variable predictiva riesgo (1, 2, 3). Se ha detectado que existen más valores que los indicados en la BD_Limpia     ^^^^^^^^\n")
        self.status = "TestPassed:)"
        self.test_meth = "test_integrity"
