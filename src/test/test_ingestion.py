# ================================= LIBRARIES  ================================= #

# importing packages
import pandas as pd
import marbles.core
from datetime import datetime
import os

# importing especific functions

# importing custom libraries

# Requires...

# ================================= FUNCTION: testing DF ================================= #

class TestIngest(marbles.core.TestCase):
    
    # Variables
    todate = datetime.date(datetime.today())
    test_meth = ''
    status = ''
    err_msg = ''

    __name__ = 'TestIngest'
    
    def test_df_not_empty(self):
        
        data = pd.read_csv('src/test/trans_file.csv', header = None).iloc[0,0]
        print(data)
        df = pd.read_json(data)
        df_sh = df.shape
        
        self.assertGreater(df_sh[0], 0, note = "Los descarga de datos de la API de CFI está vacía. Posiblemente la fecha a \
                           ingestar es posterior a la fecha actual.")
        self.status = "TestPassed:)"
        self.test_meth = "test_df_not_empty"
        
        