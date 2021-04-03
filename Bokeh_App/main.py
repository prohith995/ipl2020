# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 19:19:34 2020

@author: nxf55806
"""

import pandas as pd

# os methods for manipulating paths
from os.path import dirname, join

# Bokeh basics 
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

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


# Each tab is drawn by one script
from plot import get_dataset
from plot import make_plot
from plot import update_plot


