# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 17:58:34 2020

@author: nxf55806
"""

import pandas as pd

df_match2 = pd.read_csv("Raw_Data/kaggle2_matches.csv")
df_deliveries2 = pd.read_csv("Raw_Data/kaggle2_deliveries.csv")

last_match_id = df_deliveries2['match_id'].max()
list(df_deliveries2)

def batsman_stats(data, batsman):
    x = data[data['batsman'] == batsman]
    initial_cols = list(x.columns)

    matches = x['match_id'].nunique()
    runs = sum(x['total_runs'])
    balls = len(x)
    dismissals = len(data[data['player_dismissed'] == batsman])
    
    x['Matches'] = matches
    x['Runs'] = runs
    if dismissals == 0:
        x['Average'] = runs
    else:
        x['Average'] = runs/matches
    if balls == 0:
        x['Strike_Rate'] = 0
    else:
        x['Strike_Rate'] = runs*100/balls
    x['4s'] = len(x[x['batsman_runs'] == 4])
    x['6s'] = len(x[x['batsman_runs'] == 6])
    if matches == 0:
        x['4s_average'] = 0
        x['6s_average'] = 0
    else:
        x['4s_average'] = x['4s'].iloc[0]/matches
        x['6s_average'] = x['6s'].iloc[0]/matches
    x['not_outs'] = matches - dismissals
    
    return x.drop(columns = [i for i in initial_cols]).iloc[0]

def batsman_previous_stats(match_id, batsman):
    prev_matches = df_deliveries2[df_deliveries2['match_id'] < match_id]
    total_stats = batsman_stats(prev_matches, batsman)
    if len(prev_matches[prev_matches['inning'] == 1]) != 0:
        inn1_stats = batsman_stats(prev_matches[prev_matches['inning'] == 1], batsman)
        inn1_stats.index = [i+'_Inn1' for i in inn1_stats.index]
        total_stats = pd.concat([total_stats, inn1_stats])    
    if len(prev_matches[prev_matches['inning'] == 2]) != 0:
        inn2_stats = batsman_stats(prev_matches[prev_matches['inning'] == 2], batsman)
        inn2_stats.index = [i+'_Inn2' for i in inn2_stats.index]
        total_stats = pd.concat([total_stats, inn2_stats])    
    return total_stats

batsman_overall_stats = {}
for batsman in df_deliveries2['batsman'].unique():
    batsman_overall_stats[batsman] = batsman_previous_stats(last_match_id, batsman)
match_id = last_match_id


x = df_deliveries2[df_deliveries2['batsman'] == batsman]
data = df_deliveries2
    
df_final = pd.DataFrame()
def match_player_data(x):
    global last_match_id
    # match_id = 250
    # batsman = 'LRPL Taylor'
    match_id = x['match_id'].iloc[0]
    batsman = x['batsman'].iloc[0]
    prev_stats = batsman_previous_stats(match_id, batsman)
    overall_stats = batsman_overall_stats[batsman]
    
    
df_deliveries2.groupby(['match_id', 'batsman']).apply(match_player_data)



