# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 21:40:07 2020

@author: nxf55806
"""

import pandas as pd

matches = pd.read_csv("Raw_Data/kaggle2_matches.csv")
balls = pd.read_csv("Raw_Data/kaggle2_deliveries.csv")

list(matches)
list(balls)

df = pd.merge(matches[['id', 'season', 'city', 'venue']],
              balls[['match_id', 'inning', 'batting_team', 'bowling_team', 'over', 'batsman', 
                     'non_striker', 'bowler', 'batsman_runs']],
              left_on='id', right_on='match_id', how='right')
list(df)
df.drop(columns=['id', 'venue', 'match_id'], inplace=True)
