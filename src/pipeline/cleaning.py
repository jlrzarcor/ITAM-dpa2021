#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 10:44:03 2021

@author: urieluard
"""
import pickle
import pandas as pd
import numpy as np

def standarize_column_strings(df, columns, excluded_punctuation=".,*¿?¡!"):
    for col in columns:
        df[col] = df[col].str.lower().astype(str).str.replace(" ", "_")
        df[col] = df[col].str.lower().astype(str).str.replace("-", "_")
        df[col] = df[col].str.lower().astype(str).str.replace("á", "a")
        df[col] = df[col].str.lower().astype(str).str.replace("é", "e")
        df[col] = df[col].str.lower().astype(str).str.replace("í", "i")
        df[col] = df[col].str.lower().astype(str).str.replace("ó", "o")
        df[col] = df[col].str.lower().astype(str).str.replace("ú", "u")
        df[col] = df[col].str.lower().astype(str).str.replace("ü", "u")
        df[col] = df[col].str.lower().astype(str).str.replace(r"[^a-zA-Z\d\_]+", "")
        for ch in excluded_punctuation:
            df[col] = df[col].str.replace(ch, "")

def cleaning(df):
    '''
    Función que convierte las columnas del Data Frame al tipo y forma que se necesita para
    los análisis posteriores
    
    inputs: Data Frame almacenado en el S3 (ingesta.pkl)
    outputs: Data Frame con las variables en formato adecuado (df_clean.pkl)
        
    '''
    df = pickle.load(open("ingesta.pkl","rb"))
    # Variables de texto
    df['violations']= df['violations'].astype('object')
    df['violations_count'] = df.violations.str.count(r'\|')+1
    df['violations_count'] = df.violations_count.fillna(0)
    df['violations_count'] = df['violations_count'].astype('int')
    # Variables categóricas
    df['dba_name']= df['dba_name'].astype('object')
    df['aka_name']= df['aka_name'].astype('object')
    df['facility_type']= df['facility_type'].astype('category')
    df['risk']= df['risk'].astype('category')
    df['address']= df['address'].astype('category')
    df['city']= df['city'].astype('category')
    df['state']= df['state'].astype('category')
    df['inspection_type']= df['inspection_type'].astype('category')
    df['results']= df['results'].astype('category')
    # Variable label_risk
    df['risk'] = df['risk'].replace(["Risk 1 (High)"],3)
    df['risk'] = df['risk'].replace(["Risk 2 (Medium)"],2)
    df['risk'] = df['risk'].replace(["Risk 3 (Low)"],1)
    df['risk'] = df['risk'].replace(["All"],0)
    df['risk'] = pd.to_numeric(df['risk'], errors='coerce')
    df=df.rename(columns = {'risk':'label_risk'})
    df['label_risk'] = df['label_risk'].astype('int')
    # Variables de fecha
    df['inspection_date'] = pd.to_datetime(df['inspection_date'], infer_datetime_format=True)
    df['inspection_month']=df['inspection_date'].dt.month
    MONTH = 12
    df['sin_mnth'] = np.sin(2*np.pi*df.inspection_month/MONTH)
    df['cos_mnth'] = np.cos(2*np.pi*df.inspection_month/MONTH)
    df['inspection_weekday']=df['inspection_date'].dt.weekday
    WEEKDAY = 7
    df['sin_wkd'] = np.sin(2*np.pi*df.inspuntitled0ection_weekday/WEEKDAY)
    df['cos_wkd'] = np.cos(2*np.pi*df.inspection_weekday/WEEKDAY)
    # Etiqueta
    df_np1 = df[df['results'] == 'Fail']
    df_np1['label_results'] = 0
    df_np2 = df[df['results'] == 'Pass']
    df_np2['label_results'] = 1
    df_np3 = df[df['results'] == 'Pass w/ Conditions']
    df_np3['label_results'] = 1
    df_np4 = df[df['results'] == 'Business Not Located']
    df_np4['label_results'] = 2
    df_np5 = df[df['results'] == 'No Entry']
    df_np5['label_results'] = 2
    df_np6 = df[df['results'] == 'Not Ready']
    df_np6['label_results'] = 2
    df_np7 = df[df['results'] == 'Out of Business']
    df_np7['label_results'] = 2
    df = df_np1.append(df_np2).append(df_np3).append(df_np4).append(df_np5).append(df_np6).append(df_np7)
    # Imputación de datos
    df.drop(['violations'],axis = 1, inplace = True)
    df.drop(['results'], axis = 1, inplace = True)
    df.drop(df.loc[df['license'].isnull()].index, inplace=True)
    df.drop(df.loc[df['zip'].isnull()].index, inplace=True)
    df['risk'] = df['risk'].fillna(0)
    df.drop(df.loc[df['label_results'] == 2].index, inplace=True)
    df['aka_name'] = df['aka_name'].fillna(df['dba_name'])
    df['dba_name']= df['dba_name'].astype(str).str.lower()
    df['aka_name']= df['aka_name'].astype(str).str.lower()
    df['facility_type']= df['facility_type'].astype(str).str.lower()
    df['state']= df['state'].astype(str).str.lower()
    df['inspection_type']= df['inspection_type'].astype(str).str.lower()
    df = df[~df['state'].isin(['wi', 'ny', 'in'])]
    col_text = ['dba_name','aka_name']
    standarize_column_strings(df, col_text)
    df_dict_dummy = pd.DataFrame(df['aka_name'])
    df_dict_dummy['facility_type'] = df['facility_type']
    df_dict_dummy.drop(df_dict_dummy.loc[df_dict_dummy['facility_type'].isnull()].index, inplace=True)
    group = df_dict_dummy.groupby('aka_name')
    df_dict_dummy2 = group.apply(lambda x: x['facility_type'].unique())
    df_dict_dummy3 = df_dict_dummy2.to_frame()
    df_dict_dummy3.reset_index(level = 'aka_name', inplace = True)
    df_dict_dummy3 = df_dict_dummy3.rename(columns = {0:'facility_type'})
    df_dict_dummy3['facility_type'] = df_dict_dummy3['facility_type'].apply(lambda x: str(x[0]))
    df2 = pd.merge(df,df_dict_dummy3, how = 'left', on = 'aka_name')
    df2['facility_type_x'] = df2['facility_type_x'].fillna(df2['facility_type_y'])
    df2['facility_type_x'] = df2['facility_type_x'].fillna('restaurant')
    df2=df2.rename(columns = {'facility_type_x':'facility_type'})
    df2.drop(['inspection_id','dba_name','address','city','state','latitude','longitude','location','facility_type_y','inspection_weekday','inspection_month'],axis = 1, inplace = True)
    pickle.dump(df2,open("df_clean.pkl","wb"))
    return df2

