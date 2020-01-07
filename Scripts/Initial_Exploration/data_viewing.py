#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 14:53:35 2020

@author: rohith
"""

import pandas as pd

df_match = pd.read_csv("Raw_Data/kaggle_match_data.csv")
df_innings = pd.read_csv("Raw_Data/kaggle_innings_data.csv")

df_match2 = pd.read_csv("Raw_Data/kaggle2_matches.csv")
df_deliveries2 = pd.read_csv("Raw_Data/kaggle2_deliveries.csv")

list(df_match)
list(df_match2)

list(df_innings)
list(df_deliveries2)

high_sr_batsmen = (df_deliveries2.groupby('batsman')
                       .agg({'total_runs':'mean', 'ball':'count'})
                       .rename(columns = {"total_runs":"Strike_Rate", "ball":"Total_Balls"})
                       .sort_values('Strike_Rate', ascending=False))
high_sr_batsmen.Strike_Rate = high_sr_batsmen.Strike_Rate * 100
high_sr_batsmen = high_sr_batsmen[high_sr_batsmen.Total_Balls > 100]

df_final_deliveries = df_deliveries2[df_deliveries2.over > 15] 
finishing_batsmen = (df_final_deliveries.groupby('batsman')
                     .agg({'total_runs':['sum','mean'], 'ball':'count'}))
finishing_batsmen.columns = finishing_batsmen.columns.droplevel()

finishing_batsmen = finishing_batsmen.rename(columns = {"sum":"Runs", "mean":"Strike_Rate", "count":"Total_Balls"}).sort_values('Strike_Rate', ascending=False).reset_index()
finishing_batsmen.Strike_Rate = finishing_batsmen.Strike_Rate * 100
finishing_batsmen = finishing_batsmen[finishing_batsmen.Total_Balls > 50]


r3 = df_final_deliveries.groupby('batsman').agg({'total_runs':['sum','mean'], 'ball':'count'})
r3.columns = r3.columns.droplevel()

 