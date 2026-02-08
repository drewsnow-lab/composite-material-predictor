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
num_scaler = pickle.load(open('../flaskAPP/tech_models/num_scaler_1.pkl', 'rb'))
#with open('../flaskAPP/tech_models/num_scaler.pkl', 'rb') as f:
   # num_scaler = pickle.load(f)
#Random Forest для упругости
rf1 = pickle.load(open('../flaskAPP/ml_models/rf1_1.pkl', 'rb'))
#with open('../flaskAPP/ml_models/rf1.pkl', 'rb') as f:
   # rf1 = pickle.load(f)
#GradientBusting для растяжения
gb2 = pickle.load(open('../flaskAPP/ml_models/gb2_1.pkl', 'rb'))
#with open('../flaskAPP/ml_models/gb2.pkl', 'rb') as f:
   # gb2 = pickle.load(f)


print ("models loaded success")
#app
app = Flask(__name__)
#route
@app.route('/', methods = ['POST', 'GET'])
def main():
   #отображение формы анкеты по умолчанию
   if request.method == 'GET':
      return render_template('main.html')
   #если пользователь отправил форму с веб-страницы
   if request.method == 'POST':
      #print ("страница в разработке")

      #get data from form
      ratio_matrix_filler = request.form['Соотношение матрица-наполнитель']
      density = request.form['Плотность, кг/м3']
      elastify_modulus = request.form['модуль упругости, ГПа']
      curing_agent = request.form['Количество отвердителя, м.%']
      epoxy_groups = request.form['Содержание эпоксидных групп,%_2']
      flash_temp = request.form['Температура вспышки, С_2']
      surface_density = request.form['Поверхностная плотность, г/м2']
      elasticity_modulus = request.form['Модуль упругости при растяжении, ГПа']
      resin_consumption = request.form['Потребление смолы, г/м2']
      stitch_angle = request.form['Угол нашивки, град']
      stitch_step = request.form['Шаг нашивки']
      stitch_density_log = request.form['Плотность нашивки_лог']

      #get preprocessing
      ##num
      x_num = [float(ratio_matrix_filler), float(density), float(elastify_modulus), float(curing_agent),
       float(epoxy_groups), float(flash_temp), float(surface_density), float(elasticity_modulus),
       float(resin_consumption), float(stitch_angle), float(stitch_step), float(stitch_density_log)]
      
      #scaler
      X_scaled = num_scaler.transform([x_num])
      print('X_scaled:', X_scaled)

      #predict
      predicted_value = gb2.predict(X_scaled)
      prediction = float(predicted_value[0])
      prediction_formatted = round(prediction, 2)
      #return result
      result_message = f"Прочность при растяжении, МПа: {prediction_formatted}"
      
      return render_template('main.html', result = result_message)



if __name__ == '__main__':
    app.run(debug=True)
