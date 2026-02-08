#import
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import GradientBoostingRegressor
import tensorflow as tf

from sklearn.cluster import KMeans
import pickle #для сохранения моделей
from flask import (Flask, # сервер
                   render_template, # отображение шаблонов 
                   request, #обработка запросов
                   jsonify)  #для отработки APi запросов и возвращение в фомрате JSON
print("import success")
#load models
#Scaler
num_scaler = pickle.load(open('../flaskAPP/tech_models/num_scaler.pkl', 'rb'))
#with open('../flaskAPP/tech_models/num_scaler.pkl', 'rb') as f:
   # num_scaler = pickle.load(f)
#Random Forest для упругости
rf1 = pickle.load(open('../flaskAPP/ml_models/rf1.pkl', 'rb'))
#with open('../flaskAPP/ml_models/rf1.pkl', 'rb') as f:
   # rf1 = pickle.load(f)
#GradientBusting для растяжения
gb2 = pickle.load(open('../flaskAPP/ml_models/gb2.pkl', 'rb'))
#with open('../flaskAPP/ml_models/gb2.pkl', 'rb') as f:
   # gb2 = pickle.load(f)


print ("models loaded success")
#app
app = Flask(__name__)
#route

#get data


#get preprocessing


#categorical

##num


#X


#scaler


#predict


#return result
#if __name__ == '__main__':
 #   app.run(debug=True)