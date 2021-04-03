# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 19:08:29 2020

@author: nxf55806
"""

import pickle
import pandas as pd
with open('Data/2020_auction_data', 'rb') as file:
    df = pickle.load(file)
    
player_stats = df.groupby(['player', 'year']).agg({'score_batting':'sum', 'score_bowling':'sum', 'score_fielding':'sum', 'total_score':'sum'}).reset_index()
top_stats = df.groupby(['year', 'player']).agg({'score_batting':'sum', 'score_bowling':'sum', 'score_fielding':'sum', 'total_score':'sum'}).reset_index()


player_stats
player_stats.to_excel('Data/2020_auction_data.xlsx', index=False)
