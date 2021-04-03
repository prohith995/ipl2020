# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 15:18:51 2020

@author: nxf55806
"""

import pandas as pd
import pickle

df_match2 = pd.read_csv("Raw_Data/kaggle2_matches.csv")
df_deliveries2 = pd.read_csv("Raw_Data/kaggle2_deliveries.csv")

df_match2['date'] = pd.to_datetime(df_match2['date'])
df_match2.sort_values('date', inplace=True)
df_match2 = df_match2.reset_index(drop=True).reset_index().rename(columns={"index":"match_id_ordered", "id":"match_id"})
df_deliveries2 = pd.merge(df_deliveries2, df_match2[['match_id','match_id_ordered', 'season']],
                          on = 'match_id', how='left')
df_deliveries2.sort_values(['match_id_ordered', 'over', 'ball'], inplace=True)

fantasy_rules_batsman = {'Runs_points':1, '4_bonus':1, '6_bonus':2, 'half_century_bonus':8,
                         'century_bonus':16, 'strike_rate_70_penalty':2, 'duck_penaly':2}
fantasy_rules_bowler = {'Wicket_points':25, '4_wicket':8, '5_wicket':16, 'maiden':8,
                          'above_11':6, '10-11':4, '9-10':2, 'below_4':6, '4-5':4, '5-6':2,}
fantasy_rules_fielder = {'catch':8, 'run_out_stump':12}

def batsman_match_score(batsman, match_id):
    global df_deliveries2, fantasy_rules_batsman
    x = df_deliveries2[(df_deliveries2['match_id_ordered'] == match_id) & (df_deliveries2['batsman'] == batsman)]
    runs = sum(x['batsman_runs'])
    balls = len(x)
    fours = len(x[x['batsman_runs'] == 4])
    sixes = len(x[x['batsman_runs'] == 6])
    strike_rate_less = runs/balls < 0.7
    dismissals = len(x[x['player_dismissed'] == batsman])
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

def bowler_match_score(bowler, match_id):
    global df_deliveries2, fantasy_rules_bowler
    x = df_deliveries2[(df_deliveries2['match_id_ordered'] == match_id) & (df_deliveries2['bowler'] == bowler)]
    runs = sum(x['total_runs'])
    balls = len(x)
    wickets = sum((x['dismissal_kind'].apply(lambda x: x in ['bowled', 'caught', 'caught and bowled', 'hit wicket', 'lbw', 'stumped']).astype(int)))
    four_wicket = wickets >= 4
    five_wicket = wickets >= 5
    maidens = sum((x.groupby(['over'])['total_runs'].sum() == 0).astype(int))
    
    strike_rate = runs/balls    
    if strike_rate < 4 :
        strike_rate_score = fantasy_rules_bowler['below_4']
    elif strike_rate < 5 :
        strike_rate_score = fantasy_rules_bowler['4-5']
    elif strike_rate <= 6 :
        strike_rate_score = fantasy_rules_bowler['5-6']
    elif strike_rate > 11 :
        strike_rate_score = fantasy_rules_bowler['above_11']
    elif strike_rate > 10 :
        strike_rate_score = fantasy_rules_bowler['10-11']
    elif strike_rate >= 9 :
        strike_rate_score = fantasy_rules_bowler['9-10']
    else :
        strike_rate_score = 0

    total_score = (wickets*fantasy_rules_bowler['Wicket_points'] 
                   + four_wicket*fantasy_rules_bowler['4_wicket'] 
                   + five_wicket*fantasy_rules_bowler['5_wicket'] 
                   + maidens*fantasy_rules_bowler['maiden'] 
                   + strike_rate_score)
    return total_score

def fielder_match_score(fielder, match_id):
    global df_deliveries2, fantasy_rules_fielder
    x = df_deliveries2[(df_deliveries2['match_id_ordered'] == match_id) & (df_deliveries2['fielder'] == fielder)]
    catches = len(x[(x['dismissal_kind'] == 'caught') | (x['dismissal_kind'] == 'caught and bowled')])
    stumps_and_runouts= len(x[(x['dismissal_kind'] == 'stumped') | (x['dismissal_kind'] == 'run out')])
    
    total_score = (catches*fantasy_rules_fielder['catch'] 
                   + stumps_and_runouts*fantasy_rules_fielder['run_out_stump'])
    return total_score


df_batting = pd.DataFrame()
def match_batsmen_score(x):
    global df_match2
    global df_batting

    season = x['season'].iloc[0]
    match_id = x['match_id_ordered'].iloc[0]
    batsman = x['batsman'].iloc[0]
    print(match_id, batsman)

    all_details = pd.Series([season, match_id, batsman], index=['year', 'match_id_ordered', 'player'])
    all_details['score_batting'] = batsman_match_score(batsman, match_id)

    df_batting = df_batting.append(all_details, ignore_index=True) 
    
df_deliveries2.groupby(['match_id_ordered', 'batsman'], as_index=False).apply(match_batsmen_score)


df_bowling = pd.DataFrame()
def match_bowler_score(x):
    global df_match2
    global df_bowling

    season = x['season'].iloc[0]
    match_id = x['match_id_ordered'].iloc[0]
    bowler = x['bowler'].iloc[0]
    print(match_id, bowler)

    all_details = pd.Series([season, match_id, bowler], index=['year', 'match_id_ordered', 'player'])
    all_details['score_bowling'] = bowler_match_score(bowler, match_id)

    df_bowling = df_bowling.append(all_details, ignore_index=True) 
    
df_deliveries2.groupby(['match_id_ordered', 'bowler'], as_index=False).apply(match_bowler_score)


df_fielding = pd.DataFrame()
def match_fielder_score(x):
    global df_match2
    global df_fielding

    season = x['season'].iloc[0]
    match_id = x['match_id_ordered'].iloc[0]
    fielder = x['fielder'].iloc[0]
    print(match_id, fielder)

    all_details = pd.Series([season, match_id, fielder], index=['year', 'match_id_ordered', 'player'])
    all_details['score_fielding'] = fielder_match_score(fielder, match_id)

    df_fielding= df_fielding.append(all_details, ignore_index=True) 
    
df_deliveries2.groupby(['match_id_ordered', 'fielder'], as_index=False).apply(match_fielder_score)

df_final = pd.merge(df_batting, df_bowling, on = ['year', 'match_id_ordered', 'player'], how = 'outer')
df_final = pd.merge(df_final, df_fielding, on = ['year', 'match_id_ordered', 'player'], how = 'outer')

df_final.fillna(0, inplace=True)

df_final = df_final[['year', 'match_id_ordered', 'player', 'score_batting', 'score_bowling', 'score_fielding']]
df_final['total_score'] = df_final['score_batting'] + df_final['score_bowling'] + df_final['score_fielding']

with open('Data/2020_auction_data', "wb") as file:
    pickle.dump(df_final, file)



