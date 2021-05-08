import pickle
import pandas as pd
import numpy as np
import time 
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
import os

def feat_eng(df_fe):
    '''
    Función que realiza la selección de los features que serán utilizdos para la clasificación
    
    inputs: Data Frame limpio (df_clean.pkl)
    outputs: Data Frame con la matriz de diseño para el modelo (df_clean.pkl)
        
    '''
    
    # Transformación de variables facility_type y zip
    tipo = pd.DataFrame(df_fe.facility_type.value_counts())
    tipo['name'] = tipo.index
    tipo.index = range(len(tipo.name))
    grupo1 = tipo.iloc[0:4,1].tolist()
    grupo2 = tipo.iloc[[5,6,7,11],1].tolist()
    df_fe['class'] = df_fe['facility_type'].apply(lambda x: x if x in grupo1 else ('daycare' if x in grupo2 else 'other'))
    lev = pd.read_csv(os.path.realpath('src/utils/zip_catalog.csv'))
    lev['zip'] = lev['zip'].astype(str)
    lev.index = lev.zip
    dic = lev.level.to_dict()
    df_fe['level'] = df_fe['zip'].apply(lambda x: zips(x,lev,dic))
    
    
    # Transformación a OHE
    df_fe = df_fe.sort_values(by='inspection_date', ascending=True)
    df_input = pd.DataFrame(df_fe[['label_risk','label_results','level','class']])
    data_input_ohe = pd.get_dummies(df_input)
    etiqueta = data_input_ohe.label_results
    data_input_ohe= data_input_ohe.drop('label_results', axis = 1)
    variables_lista = list(data_input_ohe.columns)
    # Grid Search
    np.random.seed(20201124)
    # ocuparemos un RF
    classifier = RandomForestClassifier(oob_score=True, n_jobs=-1, random_state=1234)
    # separando en train, test
    #X_train, X_test, y_train, y_test = train_test_split(data_input_ohe, etiqueta, test_size=0.3)

    # definicion de los hiperparametros que queremos probar
    hyper_param_grid = {'n_estimators': [300, 400], #'min_samples_leaf': [3,5,7],
                        'max_depth': [7, 10],
                        #'min_samples_split': [3],
                        'max_features': [3, 5, 6],
                        'criterion': ['gini']}
    # usamos TimeSeriesSplit para dividir respetando el orden cronológico
    tscv = TimeSeriesSplit(n_splits=3)
    # This was the trickiest part as a newbie. Straight from the docs
    # If you only have experience with CV splits this way
    # of making the splits might seem foreign. Fret not.
    for train_index, test_index in tscv.split(data_input_ohe):
        X_train, X_test = data_input_ohe.iloc[train_index, :], data_input_ohe.iloc[test_index,:]
        y_train, y_test = etiqueta.iloc[train_index], etiqueta.iloc[test_index]
    # ocupemos grid search
    gs = GridSearchCV(classifier, 
                           hyper_param_grid, 
                           scoring = 'precision', return_train_score=True,
                           cv = tscv)
    start_time = time.time()
    gs.fit(X_train, y_train)
    best_rf = gs.best_estimator_
    best_score = gs.best_estimator_.oob_score_
    feature_importance = pd.DataFrame({'importance':\
                                       best_rf.feature_importances_,\
                                       'feature': variables_lista})
    feature_importance=feature_importance.sort_values(by="importance", ascending=False)
    
    #fi_out = feature_importance.head(10)
    
    time_exec = time.time() - start_time
    nrows_ohe = data_input_ohe.shape[0]
    ncols_ohe = data_input_ohe.shape[1]
    
    #print("Tiempo en ejecutar: ", time.time() - start_time)
    
    return df_input, nrows_ohe, ncols_ohe, float(best_score), time_exec, str(best_rf)



def zips(x,lev,dic):
    if x in lev.zip.to_list():
        return dic[x]
    else:
        return 'other'