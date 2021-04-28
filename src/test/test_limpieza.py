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

class TestCleaning(marbles.core.TestCase):
    
    # Variables
    todate = datetime.date(datetime.today())
    test_meth = ''
    status = ''
    err_msg = ''

    __name__ = 'TestCleaning'
    
    def test_min_date(self):

        RDS_targ = pd.read_csv('src/test/trans_file.csv', header = None)
        
      # Create a DataFrame from clean data from RDS db.
        conn = psycopg2.connect(dbname = RDS_targ.iloc[0,0], user = RDS_targ.iloc[0,2], password = RDS_targ.iloc[0,3],
                                port = RDS_targ.iloc[0,4], host = RDS_targ.iloc[0,5])
        #dbtable = RDS_targ.iloc[0,1],
        str_qry = "SELECT MIN(inspection_date) AS min_insp_date, MAX(inspection_date) as max_insp_date FROM procdata.limpieza;"
        clean_data = sqlio.read_sql_query(str_qry, conn)
        init_date = datetime.date(datetime(2010, 1, 1)) 
        test_val = clean_data.iloc[0,0] > init_date
        
        self.assertTrue(test_val, note = "^^^^^^^^   Existen registros con fecha de inspección anterior a la fecha reportada por ChicagoFoodInspections   ^^^^^^^^\n")
        self.status = "TestPassed:)"
        self.test_meth = "test_min_date"