#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 11:12:36 2021

@author: urieluard
"""
import pickle
import pandas as pd
import numpy as np
import time 
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
from sklearn.ensemble import RandomForestClassifier

def feat_eng(df_clean):
    '''
    Función que realiza la selección de los features que serán utilizdos para la clasificación
    
    inputs: Data Frame limpio (df_clean.pkl)
    outputs: Data Frame con la matriz de diseño para el modelo (df_clean.pkl)
        
    '''
    df_fe = pickle.load(open("df_clean.pkl","rb"))
    
    # Transformación a OHE
    df_fe = df_fe.sort_values(by='inspection_date', ascending=True)
    df_input = pd.DataFrame(df_fe[['label_risk','label_results','zip','facility_type']])
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
                        'min_samples_split': [3],
                        'max_features': [10, 15, 20],
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
    print("Tiempo en ejecutar: ", time.time() - start_time)
    return gs.best_estimator_.oob_score_
