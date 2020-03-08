# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 17:58:34 2020

@author: nxf55806
"""

import pandas as pd
import pickle

df_match2 = pd.read_csv("Raw_Data/kaggle2_matches.csv")
df_deliveries2 = pd.read_csv("Raw_Data/kaggle2_deliveries.csv")

# last_match_id = df_deliveries2['match_id'].max()

fantasy_rules_batsman = {'Runs_points':0.5, '4_bonus':0.5, '6_bonus':1, 'half_century_bonus':4,
                         'century_bonus':8, 'strike_rate_70_penalty':3, 'duck_penaly':2}

df_match2['date'] = pd.to_datetime(df_match2['date'])
df_match2.sort_values('date', inplace=True)
df_match2 = df_match2.reset_index(drop=True).reset_index().rename(columns={"index":"match_id_ordered", "id":"match_id"})
df_deliveries2 = pd.merge(df_deliveries2, df_match2[['match_id','match_id_ordered']],
                          on = 'match_id', how='left')
df_deliveries2.sort_values(['match_id_ordered', 'over', 'ball'], inplace=True)

def batsman_stats(data, batsman):
    x = data[data['batsman'] == batsman]
    initial_cols = list(x.columns)

    matches = x['match_id_ordered'].nunique()
    runs = sum(x['batsman_runs'])
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
    prev_matches = df_deliveries2[df_deliveries2['match_id_ordered'] < match_id]
    if len(prev_matches[prev_matches['batsman'] == batsman]) != 0:
        total_stats = batsman_stats(prev_matches, batsman)
    else:
        return pd.Series()
    if len(prev_matches[(prev_matches['inning'] == 1) & (prev_matches['batsman'] == batsman)]) != 0:
        inn1_stats = batsman_stats(prev_matches[prev_matches['inning'] == 1], batsman)
        inn1_stats.index = [i+'_Inn1' for i in inn1_stats.index]
        total_stats = pd.concat([total_stats, inn1_stats])    
    if len(prev_matches[(prev_matches['inning'] == 2) & (prev_matches['batsman'] == batsman)]) != 0:
        inn2_stats = batsman_stats(prev_matches[prev_matches['inning'] == 2], batsman)
        inn2_stats.index = [i+'_Inn2' for i in inn2_stats.index]
        total_stats = pd.concat([total_stats, inn2_stats])    

    recent_matches = df_deliveries2[(df_deliveries2['match_id_ordered'] < match_id) & (df_deliveries2['match_id_ordered'] > match_id-100)]
    if len(recent_matches[recent_matches['batsman'] == batsman]) != 0:
        total_stats_recent = batsman_stats(recent_matches, batsman)
        total_stats_recent.index = [i+'_Recent' for i in total_stats_recent.index]
        total_stats = pd.concat([total_stats, total_stats_recent])    
    if len(recent_matches[(recent_matches['inning'] == 1) & (recent_matches['batsman'] == batsman)]) != 0:
        inn1_stats_recent = batsman_stats(recent_matches[recent_matches['inning'] == 1], batsman)
        inn1_stats_recent.index = [i+'_Inn1_Recent' for i in inn1_stats_recent.index]
        total_stats = pd.concat([total_stats, inn1_stats_recent])    
    if len(recent_matches[(recent_matches['inning'] == 2) & (recent_matches['batsman'] == batsman)]) != 0:
        inn2_stats_recent = batsman_stats(recent_matches[recent_matches['inning'] == 2], batsman)
        inn2_stats_recent.index = [i+'_Inn2_Recent' for i in inn2_stats_recent.index]
        total_stats = pd.concat([total_stats, inn2_stats_recent])    
    
    return total_stats

def batsman_match_score(batsman, match_id):
    global df_deliveries2, fantasy_rules_batsman
    x = df_deliveries2[(df_deliveries2['match_id_ordered'] == match_id) & (df_deliveries2['batsman'] == batsman)]
    runs = sum(x['batsman_runs'])
    balls = len(x)
    fours = len(x[x['batsman_runs'] == 4])
    sixes = len(x[x['batsman_runs'] == 6])
    dismissals = len(df_deliveries2[(df_deliveries2['match_id_ordered'] == match_id) & (df_deliveries2['player_dismissed'] == batsman)])    
    strike_rate_less = runs/balls < 0.7
    duck_out = (dismissals == 1) & (runs == 0)
    half_century = runs >= 50
    century = runs >= 100
    total_score = (runs*fantasy_rules_batsman['Runs_points'] 
                   + fours*fantasy_rules_batsman['4_bonus'] 
                   + sixes*fantasy_rules_batsman['6_bonus'] 
                   - fantasy_rules_batsman['strike_rate_70_penalty']*strike_rate_less
                   - fantasy_rules_batsman['strike_rate_70_penalty']*duck_out
                   + fantasy_rules_batsman['half_century_bonus']*half_century
                   + fantasy_rules_batsman['century_bonus']*century)
    return total_score
 
# batsman_overall_stats = {}
# for batsman in df_deliveries2['batsman'].unique():
#     batsman_overall_stats[batsman] = batsman_previous_stats(last_match_id, batsman)
# match_id = last_match_id
   
df_final = pd.DataFrame()
def match_player_data(x):
    global df_match2
    global df_final
    # global last_match_id
    match_id = x['match_id_ordered'].iloc[0]
    batsman = x['batsman'].iloc[0]
    print(match_id, batsman)
    # match_id = 1
    # batsman = 'A Choudhary'
    # x = df_deliveries2[(df_deliveries2['match_id'] == match_id) & (df_deliveries2['batsman'] == batsman)]
    prev_stats = batsman_previous_stats(match_id, batsman)
    # overall_stats = batsman_overall_stats[batsman]
    for_team = df_match2[df_match2['match_id_ordered'] == match_id].iloc[0]['team1']
    against_team = df_match2[df_match2['match_id_ordered'] == match_id].iloc[0]['team2']
    city = df_match2[df_match2['match_id_ordered'] == match_id].iloc[0]['city']
    venue = df_match2[df_match2['match_id_ordered'] == match_id].iloc[0]['venue']
    all_details = pd.Series([match_id, batsman, for_team, against_team, city, venue], index=['match_id_ordered', 'batsman', 'for_team', 'against_team', 'city', 'venue'])
    if len(prev_stats) != 0:
        all_details = pd.concat([all_details, prev_stats])
    all_details['score'] = batsman_match_score(batsman, match_id)
    df_final = df_final.append(all_details, ignore_index=True) 
    
df_deliveries2.groupby(['match_id_ordered', 'batsman'], as_index=False).apply(match_player_data)

with open('Data/match_player_data', "wb") as file:
    pickle.dump(df_final, file)
