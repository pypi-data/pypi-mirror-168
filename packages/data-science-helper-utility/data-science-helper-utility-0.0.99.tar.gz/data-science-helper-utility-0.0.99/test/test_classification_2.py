# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 18:43:56 2022

@author: User
"""


from sklearn.datasets import make_classification
import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd
from data_science_helper.model import neg_bagging_fraction__lgb_model as nbf_lgb_model
from data_science_helper import helper_classification_model as hcm
from data_science_helper import helper_general as hg
import lightgbm as lgb 
import scikitplot as skplt
import matplotlib.pyplot as plt
import os


model_name = "neg_bagging_fraction__lgb_model"
metric = "f1"
num_rounds=9999999
early_stop=200
log=0
api="train_api"
random_state=42
SESGO = 0.20
n_decimals = 6
max_iter_cls = None
#cls_ini_opt = ['Z_NOTA_M_T_MENOS_1', 'Z_NOTA_C_T_MENOS_1', 'EXTRA_EDAD_T_MENOS_1']
cls_ini_opt = []

generar_df_train = False
generar_df_test = False

force_list_cls_sin_sesgo = True
enable_cls_opt = False


specific_url = 'E:/PROYECTOS/med-student-dropout-prediction/src/_04_Modeling/modelos/20072022/01.data_input/EBR/Inicial/grados_ciclo_2/norte/X_t.csv'
X_t=pd.read_csv(specific_url, encoding="utf-8")    

ID_P_T = X_t['ID_PERSONA']
y  = X_t['DESERCION'] 
                
del X_t['DESERCION'] 
del X_t['ID_PERSONA']

test_size = hcm.get_test_size(X_t)

X_train, X_test, y_train, y_test= train_test_split(X_t, y, test_size=test_size,stratify=y,random_state=random_state)


    
params_gr_mr = {
    
     "bagging_fraction": 0.8,
     "feature_fraction": 1,
     "bagging_freq":1,
     "lambda_l1": 0,
     "lambda_l2": 0,
     "learning_rate": 0.01,
     "max_bin": 150,
     "max_depth": -1,
     "min_data_in_leaf": 20,
     "min_gain_to_split": 0,
     "num_leaves": 250, #250   EBE e inicial , 150 primaria (empeoro los resultados, se debe dejar en 31), 31 secundaria
     "path_smooth": 0,
     "lambda_l1":0
    
}


args_mdl = {"strategy":model_name,"print_consola":True,
            "X_train":X_train, "y_train": y_train, "X_test": X_test, "y_test": y_test, 
            "params":params_gr_mr, "max_iter_cls": max_iter_cls,"cls_ini_opt":cls_ini_opt,
            "enable_cls_opt" : enable_cls_opt, 
            "enable_umbral_opt":False,"metric":metric,
            "num_rounds":83,"early_stop":None,"log":log,  #  early_stop     num_rounds                    
            "api":"train_api" , "sesgo":SESGO , "random_state":random_state,
            "url":"cv_test_false_" ,"cv":True,"cv_n_split":20,
            "shuffle_cv":True,  "shuffle_cv_test_size":test_size
            }                    
#hg.validar_directorio(path_directory_model)  
print("----------------------------------")
print("ANTES DEL ENTRENAMIENTO")
print(params_gr_mr)    
print("----------------------------------")
model , kpis_train  , KPIs, kpis_opt , umbral_opt , list_cls_ini  = hcm.modelar_clasificacion_binaria(**args_mdl)

df_ = pd.DataFrame()
df_["y_prob_uno_test_cv"] = [1,2,3]
df_["y_prob_uno_test_cv2"] = [1,2]

hcm.roc_curva_cross_validation(list_path=["cv_test\\cv"],n_splits=20,url_out=None)


hcm.roc_curva_cross_validation(list_path=["cv_test_false\\cv"],n_splits=20,url_out=None)

url1 = "E:\\PROYECTOS\\med-student-dropout-prediction\\src\\_04_Modeling\\modelos\\20072022\\02.Modelo\\EBR\\Inicial\\grados_ciclo_2\\lima_metro_callao\\neg_bagging_fraction__lgb_model\\cv"
url2 = "E:\\PROYECTOS\\med-student-dropout-prediction\\src\\_04_Modeling\\modelos\\20072022\\02.Modelo\\EBR\\Inicial\\grados_ciclo_2\\norte\\neg_bagging_fraction__lgb_model\\cv"
url3 = "E:\\PROYECTOS\\med-student-dropout-prediction\\src\\_04_Modeling\\modelos\\20072022\\02.Modelo\\EBR\\Inicial\\grados_ciclo_2\\sur\\neg_bagging_fraction__lgb_model\\cv"
url4 = "E:\\PROYECTOS\\med-student-dropout-prediction\\src\\_04_Modeling\\modelos\\20072022\\02.Modelo\\EBR\\Inicial\\grados_ciclo_2\\centro\\neg_bagging_fraction__lgb_model\\cv"
url5 = "E:\\PROYECTOS\\med-student-dropout-prediction\\src\\_04_Modeling\\modelos\\20072022\\02.Modelo\\EBR\\Inicial\\grados_ciclo_2\\oriente\\neg_bagging_fraction__lgb_model\\cv"

hcm.roc_curva_cross_validation(list_path=["cv_test_false_\\cv"],n_splits=20,postfix="123")
#hcm.roc_curva_cross_validation(list_path=[url1,url2,url3,url4,url5],n_splits=5,url_out=None)

kpi_cv = hcm.kpis_cross_validation(list_path=["cv_test_false\\cv"],n_splits=20,postfix="123") # 512826 , 907403 , 

full_dirname = os.path.join("AAA", "BBB")  
