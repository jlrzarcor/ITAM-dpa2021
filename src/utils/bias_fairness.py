import pickle
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

from aequitas.group import Group
from aequitas.bias import Bias
from aequitas.fairness import Fairness
from aequitas.plotting import Plot

def bias_fair(modelo,df_train_test,df_fe):
    # Separamos los sets de entrenamiento y prueba
    # Entrenamiento
    X_train = df_train_test[df_train_test.Set == 'entrenamiento']
    y_train = X_train.etiqueta
    X_train = X_train.iloc[:,0:df_train_test.shape[1]-2]
    # Prueba
    X_test = df_train_test[df_train_test.Set == 'prueba']
    y_test = X_test.etiqueta
    X_test = X_test.iloc[:,0:df_train_test.shape[1]-2]
    predicted_scores = modelo.predict_proba(X_test)
    
    # Se conforma el DataFrame que necesita Aequitas para el sesgo e inequidad de la variable facility_type (class)
    df_dummy = pd.DataFrame()
    df_dummy['scores'] = pd.Series(predicted_scores[:,1])
    df_dummy['predic'] = np.where(df_dummy['scores'] < 0.7,0,1)
    df_aeq = pd.DataFrame()
    df_aeq['real'] = y_test
    df_aeq['prediccion'] = df_dummy.predic
    df_aeq['faciliy_type'] = df_fe['class'].tail(len(df_dummy.predic))
    # Asignamos nuevos índices y los nombres de las columnas para que los reconozca la función
    df_aeq = df_aeq.reset_index(drop=True)
    df_aeq.columns = ['label_value','score','class']
    # Se obtienen las métricas
    g = Group()
    xtab, attrbs = g.get_crosstabs(df_aeq)
    absolute_metrics = g.list_absolute_metrics(xtab)
    metrics1 = xtab[['attribute_name', 'attribute_value']+[col for col in xtab.columns if col in absolute_metrics]].round(2)
    
    # Se conforma el DataFrame que necesita Aequitas para el sesgo e inequidad de la variable zip (level)
    df_aeq2 = pd.DataFrame()
    df_aeq2['real'] = y_test
    df_aeq2['prediccion'] = df_dummy.predic
    df_aeq2['zip'] = df_fe['level'].tail(len(df_dummy.predic))
    # Asignamos nuevos índices y los nombres de las columnas para que los reconozca la función
    df_aeq2 = df_aeq2.reset_index(drop=True)
    df_aeq2.columns = ['label_value','score','level']
    # Se obtienen las métricas
    g2 = Group()
    xtab2, attrbs2 = g2.get_crosstabs(df_aeq2)
    absolute_metrics2 = g2.list_absolute_metrics(xtab2)
    metrics2 = xtab2[['attribute_name', 'attribute_value']+[col for col in xtab2.columns if col in absolute_metrics2]].round(2)
    
    df_labels = pd.DataFrame()
    df_labels['scores'] = pd.Series(predicted_scores[:,1])
    df_labels['predicted'] = np.where(df_dummy['scores'] < 0.7,0,1)
    df_labels['label'] = y_test
    
    metrics = pd.concat([metrics1,metrics2]).reset_index(drop = True)
        
    # Metadata
    n_groups = len(metrics1.attribute_value) + len(metrics2.attribute_value)
    n_attribute = metrics.attribute_name.nunique()
    
    return df_labels, metrics, n_groups, n_attribute
    