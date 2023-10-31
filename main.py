# Import required dependencies
# Import required libraries
import pandas as pd
import numpy as np
import datetime
import re
import unicodedata
import warnings
pd.options.display.max_columns = None
pd.set_option('max_rows', 5000)
pd.options.display.float_format = '{:,.2f}'.format 
warnings.filterwarnings('ignore')


# Read source dataset
spotify= 'C:\gitrepos\spotify_dataset\dataset\spotify_practica.csv'
print(spotify.shape)
print(spotify.head())


# Identify type of variables in "spotify DataFrame"
print(spotify.dtypes)


# (a) - Tagging Variables By Type
# Prefixes for variable types
# 'c_' --> Numeric Variables: Discrete & Continous
# 'v_' --> Categorical Variables
# 'd_' --> Date Type Variables
# 't_' --> Text Type Variables

c_feats = ['acousticness','danceability','duration_ms','energy',
           'instrumentalness','liveness','loudness',
           'speechiness','tempo','valence']
v_feats = ['mode','key','explicit','popularity','genero']
t_feats = ['artists','id','name','zip Code']
d_feats = ['release_date']

c_feats_new = ['c_' + x for x in c_feats]
v_feats_new = ['v_' + x for x in v_feats]
d_feats_new = ['d_' + x for x in d_feats]
t_feats_new = ['t_' + x for x in t_feats]

print(list(c_feats))
print(list(c_feats_new))

# Rename columns according to the type of variable
spotify.rename(columns=dict(zip(d_feats,d_feats_new)),inplace=True)
spotify.rename(columns=dict(zip(v_feats,v_feats_new)),inplace=True)
spotify.rename(columns=dict(zip(t_feats,t_feats_new)),inplace=True)
spotify.rename(columns=dict(zip(c_feats,c_feats_new)),inplace=True)
print(spotify.shape)
print(spotify.head())