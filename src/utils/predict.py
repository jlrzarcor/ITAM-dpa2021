import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier

def predict(df_fe, model):
    var = df_fe[['aka_name', 'license']]
    df_fe.drop(['ingest_date', 'aka_name', 'license'], axis=1, inplace=True)
    data_input_ohe = pd.get_dummies(df_fe)
    etiqueta = data_input_ohe.label_results
    data_input_ohe= data_input_ohe.drop('label_results', axis = 1)
    base = pd.DataFrame({'label_risk':0,'level_downtown':0,'level_high':0,'level_low-mid':0,'level_other':0,
                    "class_children's services facility":0,'class_daycare':0,'class_grocery store':0,
                    'class_other':0,'class_restaurant':0,'class_school':0}, index = [0])
    b  = list(base.columns)
    orig = data_input_ohe.columns.tolist()
    miss_col = []
    cont = 0

    for item in b:
        if item not in orig:
            miss_col.append(cont)
            cont = cont + 1
        else:
            cont = cont + 1
    
    for index in miss_col:
        data_input_ohe.insert(index,base.columns[index],0)
        
    predicted_scores = pd.DataFrame(model.predict_proba(data_input_ohe))
    predicted_scores['predic'] = np.where(predicted_scores[1] < 0.7,0,1)
    salida = var.loc[data_input_ohe.index,['aka_name','license']].reset_index()
    salida['score'] = predicted_scores.iloc[:,1]
    salida['prediction'] = predicted_scores.iloc[:,2]
    return salida
