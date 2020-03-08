# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 18:07:21 2020

@author: nxf55806
"""

import pickle
import pandas as pd
import numpy as np

with open('Data/match_player_data', "rb") as file:
    df = pickle.load(file)

df1 = df.groupby('batsman').size().reset_index()
df1.columns = ['batsman', 'number of data points']
req_batsmen = list(df1[df1['number of data points'] >= 5]['batsman'])

df = df[(df['match_id_ordered'] >= 100)]
df = df[df['batsman'].apply(lambda x: x in req_batsmen)]
df['city'] = df['city'].fillna('Dubai')
df.fillna(0, inplace=True)

str_cols = list(df.dtypes[(df.dtypes == object)].index)

df1 = pd.concat([df, pd.get_dummies(df[str_cols], drop_first=True)], axis=1)
df1 = df1.drop(columns = str_cols)

from sklearn.model_selection import train_test_split
df_train, df_test = train_test_split(df1, test_size=0.2, random_state = 0)

X_train = df_train.drop(columns = ['score'])
y_train = df_train['score']

X_test = df_test.drop(columns = ['score'])
y_test = df_test['score']

import statsmodels.api as sm
mod = sm.OLS(y_train, X_train)
fii = mod.fit()
p_values = fii.summary2().tables[1]['P>|t|']
table = fii.summary2().tables[1]

from sklearn.linear_model import LinearRegression

lr = LinearRegression()
lr.fit(X_train, y_train)
y_train_pred = lr.predict(X_train)
y_test_pred = lr.predict(X_test)

from sklearn import metrics
metrics.r2_score(y_train, y_train_pred)    
metrics.r2_score(y_test, y_test_pred)    

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV

cv_grid = {'n_estimators': [50, 100, 250],
               'max_features': [10, 20],
               'max_depth': [20, 40],
               'min_samples_split': [2, 4],
               'min_samples_leaf': [1, 3],
               'bootstrap': [True]}

cv_grid_2 = {'n_estimators': [100, 250, 500, 1000],
               'max_features': [25, 60, 120, 250],
               'max_depth': [50, 75, 120, 250],
               'min_samples_split': [2, 4, 8, 16],
               'min_samples_leaf': [1, 3, 6, 12],
               'bootstrap': [True, False]}

rf = RandomForestRegressor()
rf_cv = GridSearchCV(rf, cv_grid)
rf_cv.fit(X_train, y_train)
rf_cv.best_params_

rf_cv_2 = GridSearchCV(rf, cv_grid_2)
rf_cv_2.fit(X_train, y_train)
rf_cv_2.best_params_

rf = RandomForestRegressor(n_estimators = 700, max_features= 100, max_depth= 75,
                           min_samples_split= 2, min_samples_leaf= 1, bootstrap= True)
rf.fit(X_train, y_train)
y_train_pred = rf.predict(X_train)
y_test_pred = rf.predict(X_test)

def mean_absolute_percentage_error(y_true, y_pred): 
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

metrics.r2_score(y_train, y_train_pred)
metrics.r2_score(y_test, y_test_pred)    
mean_absolute_percentage_error(y_train, y_train_pred)
mean_absolute_percentage_error(y_test, y_test_pred)    
