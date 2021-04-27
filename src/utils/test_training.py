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
        max_label = max(df.etiqueta)
        
        try:
            self.assertGreater(max_label, param_label, note = "La etiqueta de la matriz de entrenamiento \
                                                               no es binaria")
            self.status = "TestPassed :)"
            self.test_meth = "Labels ok"
        except Exception as excepttest:
            self.status = "TestFailed :("
            self.err_msg = excepttest