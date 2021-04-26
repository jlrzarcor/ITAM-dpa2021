import pandas as pd
from sklearn.model_selection import TimeSeriesSplit

def train(df_fe):
    # Aplicamos OneHot Encoding
    data_input_ohe = pd.get_dummies(df_fe)
    etiqueta = data_input_ohe.label_results
    data_input_ohe= data_input_ohe.drop('label_results', axis = 1)
    variables_lista = list(data_input_ohe.columns)
    # Hacemos TimeSeriesSplit para obtener las matrices de entrenamiento y prueba
    tscv = TimeSeriesSplit(n_splits=3)
    for train_index, test_index in tscv.split(data_input_ohe):
        X_train, X_test = data_input_ohe.iloc[train_index, :], data_input_ohe.iloc[test_index,:]
        y_train, y_test = etiqueta.iloc[train_index], etiqueta.iloc[test_index]
    # Metadata de las matrices para el modelo
    nrows_train = X_train.shape[0]
    nrows_test = X_test.shape[0]
    meta_train = pd.DataFrame({'nrows_train' : nrows_train,
                           'nrows_test' : nrows_test}, index = [0])
    # Hacemos un solo DF para los Datasets de Entrenamiento y Prueba y con la etiqueta
    X_train_1 = X_train_1.assign(Set = 'entrenamiento')
    X_train_1 = X_train_1.assign(etiqueta = y_train)
    X_test_1 = X_test_1.assign(Set = 'prueba')
    X_test_1 = X_test_1.assign(etiqueta = y_test)
    df_train_test = pd.concat([X_train_1, X_test_1], axis = 0)
    return df_train_test, nrows_train, nrows_test
