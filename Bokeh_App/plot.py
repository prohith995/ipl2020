# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 19:17:35 2020

@author: nxf55806
"""


# Import required packages
import pickle
import pandas as pd
import numpy as np
import os
os.chdir('C:/Users/nxf55806/Documents/Personal/Github/ipl2020/Bokeh_App')
pd.options.mode.chained_assignment = None 

from bokeh.plotting import figure
from bokeh.io import output_notebook, show
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, HoverTool, LinearColorMapper, Select
output_notebook()

from bokeh.io import curdoc, install_notebook_hook
from bokeh.layouts import column, row
from bokeh.client import push_session, pull_session

from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application

from tornado.ioloop import IOLoop

from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.server.server import Server


with open('Data/2020_auction_data', 'rb') as file:
    df = pickle.load(file)
    
player_stats = df.groupby(['player', 'year']).agg({'score_batting':'sum', 'score_bowling':'sum', 'score_fielding':'sum', 'total_score':'sum'}).reset_index()
top_stats = df.groupby(['year', 'player']).agg({'score_batting':'sum', 'score_bowling':'sum', 'score_fielding':'sum', 'total_score':'sum'}).reset_index()

top_10 = top_stats.sort_values(['year', 'total_score'], ascending=False).groupby('year', as_index=False).apply(lambda x: x.iloc[:10]).reset_index(drop=True).groupby('year')['total_score'].mean().reset_index()
top_10_to_50 = top_stats.sort_values(['year', 'total_score'], ascending=False).groupby('year', as_index=False).apply(lambda x: x.iloc[10:50]).reset_index(drop=True).groupby('year')['total_score'].mean().reset_index()
top_50_to_100 = top_stats.sort_values(['year', 'total_score'], ascending=False).groupby('year', as_index=False).apply(lambda x: x.iloc[50:100]).reset_index(drop=True).groupby('year')['total_score'].mean().reset_index()

top_10.columns = ['year', 'top 10']
top_10_to_50.columns = ['year', 'top 10-50']
top_50_to_100.columns = ['year', 'top 50-100']

player_stats = pd.merge(player_stats, top_10, on='year', how='left')
player_stats = pd.merge(player_stats, top_10_to_50, on='year', how='left')
player_stats = pd.merge(player_stats, top_50_to_100, on='year', how='left')

player_stats['year1'] = player_stats['year'] + 0.2
player_stats['year2'] = player_stats['year'] + 0.4
player_stats['year3'] = player_stats['year'] + 0.6

new_players = list(player_stats[player_stats['year'] >= 2016].player.unique())
good_players = list(player_stats[player_stats['total_score'] >= 150].player.unique())
player_stats = player_stats[player_stats['player'].apply(lambda x: x in new_players and x in good_players)] 


def get_dataset(data, player):
    df = data[data.player == player].copy()
    del df['player']

    return ColumnDataSource(data=df)

def make_plot(source, title):
    plot = figure(plot_width=800, tools="", toolbar_location=None)
    plot.title.text = title

    plot.vbar_stack(['score_batting', 'score_bowling', 'score_fielding'], x='year', color = ['orange', 'blue', 'black'], width=0.2, fill_alpha = 0.7, line_color=None, source=source)#, legend_label="Player Score")
    plot.vbar(top = 'top 10', x='year1', color = 'green', width=0.2, fill_alpha = 0.3, line_color=None, source=source)#, legend_label="top_10")
    plot.vbar(top = 'top 10-50', x='year2', color = 'green', width=0.2, fill_alpha = 0.2, line_color=None, source=source)#, legend_label="top_10-50")
    plot.vbar(top = 'top 50-100', x='year3', color = 'green', width=0.2, fill_alpha = 0.1, line_color=None, source=source)#, legend_label="top_50-100")

    plot.xaxis.axis_label = 'Year'
    plot.yaxis.axis_label = "Score"
    plot.axis.axis_label_text_font_style = "bold"
#     plot.x_range = DataRange1d(range_padding=0.0)
    plot.grid.grid_line_alpha = 1

    return plot

def update_plot(attrname, old, new):
    player = player_select.value
    plot.title.text = "Score Data for " + player

    src = get_dataset(player_stats, player)
    source.data.update(src.data)


player = 'Yuvraj Singh'    
player_select = Select(value=player, title='Player', options=list(player_stats.player.unique()))

source = get_dataset(player_stats, player)
plot = make_plot(source, "Score Data for " + player)

player_select.on_change('value', update_plot)

controls = column(player_select)
curdoc().add_root(row(plot, controls))
curdoc().title = "Score"









