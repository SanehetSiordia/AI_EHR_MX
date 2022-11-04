import pandas as pd
import os.path as path

def data_read(Name):
    result=None
    db=None
    accept=False

    if path.exists(str(Name)+'.csv'):
        db = pd.read_csv(str(Name)+'.csv')
        accept=True
        result = [accept, db]
        return result
    else:
        print("Error Archivo NO encontrado")
        result = [accept, db]
        return result