# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 14:02:39 2020

@author: nxf55806
"""

import pandas as pd

df_match = pd.read_csv("Raw_Data/kaggle_match_data.csv")
df_innings = pd.read_csv("Raw_Data/kaggle_innings_data.csv")

df_match2 = pd.read_csv("Raw_Data/kaggle2_matches.csv")
df_deliveries2 = pd.read_csv("Raw_Data/kaggle2_deliveries.csv")


list(df_match2)
list(df_innings)
list(df_deliveries2)
df_deliveries2.head()
r1 = df_innings.head()
r2 = df_deliveries2.head()

c = 0
def batsman_stats(x):
    global c
    c+=1
    print(c)
    initial_cols = list(x.columns)
    batsman = x.iloc[0]['batsman']

    x['Runs'] = sum(x['total_runs'])
    if len(x[x['player_dismissed'] == batsman]) == 0:
        x['Average'] = x.iloc[0]['Runs']
    else:
        x['Average'] = x.iloc[0]['Runs']/len(x[x['player_dismissed'] == batsman])
    x['Strike_Rate'] = x.iloc[0]['Runs']*100/len(x)
    x['4s'] = len(x[x['batsman_runs'] == 4])
    x['4s_average'] = x['4s'].iloc[0]/x['match_id'].nunique()
    x['6s'] = len(x[x['batsman_runs'] == 6])
    x['6s_average'] = x['6s'].iloc[0]/x['match_id'].nunique()

    x1 = x[x['inning'] == 1]
    x['Inn1_Runs'] = sum(x1['total_runs'])
    if len(x1[x1['player_dismissed'] == batsman]) == 0:
        x['Inn1_Average'] = x.iloc[0]['Inn1_Runs']
    else:
        x['Inn1_Average'] = x.iloc[0]['Inn1_Runs']/len(x1[x1['player_dismissed'] == batsman])
    x['Inn1_Strike_Rate'] = x['Inn1_Runs'].iloc[0]*100/len(x1)
    x['Inn1_4s'] = len(x1[x1['batsman_runs'] == 4])
    x['Inn1_4s_average'] = x['Inn1_4s'].iloc[0]/x1['match_id'].nunique()
    x['Inn1_6s'] = len(x1[x1['batsman_runs'] == 6])
    x['Inn1_6s_average'] = x['Inn1_6s'].iloc[0]/x1['match_id'].nunique()
    
    x2 = x[x['inning'] == 2]
    x['Inn2_Runs'] = sum(x2['total_runs'])
    if len(x2[x2['player_dismissed'] == batsman]) == 0:
        x['Inn2_Average'] = x.iloc[0]['Inn2_Runs']
    else:
        x['Inn2_Average'] = x['Inn2_Runs'].iloc[0]/len(x2[x2['player_dismissed'] == batsman])
    x['Inn2_Strike_Rate'] = x['Inn2_Runs'].iloc[0]*100/len(x2)
    x['Inn2_4s'] = len(x2[x2['batsman_runs'] == 4])
    x['Inn2_4s_average'] = x['Inn2_4s'].iloc[0]/x2['match_id'].nunique()
    x['Inn2_6s'] = len(x2[x2['batsman_runs'] == 6])
    x['Inn2_6s_average'] = x['Inn2_6s'].iloc[0]/x2['match_id'].nunique()
    
    return x.drop(columns = [i for i in initial_cols if i != 'batsman']).iloc[0]

batsman_stats1 = df_deliveries2.groupby('batsman', as_index=False).apply(batsman_stats)
df_deliveries2['batsman'].nunique()

initial_cols = list(df_deliveries2.columns)
[i for i in initial_cols if i != 'batsman']
