from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.tree import DecisionTreeClassifier
import time
import pandas as pd
import pickle

def model(df_train_test):
    # Funciones para regresar el DataFrame con las etiquetas y los sets de entrenamiento y 
    # y prueba a los cuatro DF X_train, Y_train, X_test y Y_test
    X_train = df_train_test[df_train_test.Set == 'entrenamiento']
    y_train = X_train.etiqueta
    X_train = X_train.iloc[:,0:df_train_test.shape[1]-2]
    X_test = df_train_test[df_train_test.Set == 'prueba']
    #y_test = X_test.etiqueta
    X_test = X_test.iloc[:,0:df_train_test.shape[1]-2]
    # Algoritmos a evaluar: DecisionTree y RandomForest
    algorithms_dict = {'tree': 'tree_grid_search'}
    algorithms = ['tree']
    # Hiperparámetros a evaluar en cada algoritmo:
    grid_search_dict = {'tree_grid_search': {'max_depth': [5,10,15], 
                                         'min_samples_leaf': [3,5,7]}}
    # Configuraciones generales de cada algoritmo a evaluar:
    estimators_dict = {'tree': DecisionTreeClassifier(random_state=1111)}
    best_estimators = []
    # Magic loop
    tscv = TimeSeriesSplit(n_splits=3)
    start_time = time.time()
    for algorithm in algorithms:
        estimator = estimators_dict[algorithm]
        grid_search_to_look = algorithms_dict[algorithm]
        grid_params = grid_search_dict[grid_search_to_look]
        gs = GridSearchCV(estimator, grid_params, scoring='precision', cv=tscv, n_jobs=-1)
        #train
        gs.fit(X_train, y_train)
        #best estimator
        best_estimators.append(gs)
    
    # MEtadata:
    # Mejor modelo de árbol
    best_tree = best_estimators[0].best_estimator_
    # Tiempo de ejecución
    t_exec = time.time() - start_time
    # Información de los modelos considerados en la selección
    r = pd.DataFrame(best_estimators[0].cv_results_)
    r = r.sort_values("rank_test_score")
    lista = r.params.astype(str)
    test_mod = "|".join(lista)
    lista_2 = r.mean_test_score.astype(str)
    mean_scores = "|".join(lista_2)
    lista_3 = r.rank_test_score.astype(str)
    rank_model = "|".join(lista_3)
    # Persistir mejor modelo en .pkl
    best_tree.fit(X_train, y_train)
    pickle.dump(best_tree, open("best_model.pkl", 'wb'))
    model_pkl = pickle.load(open("best_model.pkl","rb"))
    return model_pkl, best_tree, t_exec, test_mod, mean_scores, rank_model