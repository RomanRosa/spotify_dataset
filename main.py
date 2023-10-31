# Import required dependencies
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


# (A) - Tagging Variables By Type
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

# (B) DELETE DUPLICATES
    # Approach: Delete Duplicates Using: duplicated()
spotify.duplicated()
spotify[spotify.duplicated()]
spotify.drop_duplicates(inplace = True)

# Verify if duplicate records were deleted
spotify.duplicated().sum()

# Create a new index and delete the previous one
spotify.reset_index(drop = True, inplace = True)

# Verify dataframe shape after remove duplicates
print(spotify.shape)
print(spotify.head())

# (C) DATA COMPLETENESS
# Function used to get completeness values
# The input/argument is --> spotify
def completeness(dataframe):
    comp = pd.DataFrame(dataframe.isnull().sum())
    comp.reset_index(inplace = True)
    comp = comp.rename(columns = {'index':'column', 0:'total'})
    comp['completeness'] = (1 - comp['total']/dataframe.shape[0])*100
    comp = comp.sort_values(by = 'completeness', ascending = True)
    comp.reset_index(drop = True, inplace = True)
    return comp

# Apply "completeness function" to spotify dataframe
completeness(spotify)

# (D) Delete Variables With >=20% of Missing Value
# Drop columns with 20% or more missing values
spotify.drop(columns = ['v_explicit', 'v_key'], inplace = True)
spotify.reset_index(drop = True, inplace = True)
print(spotify.shape)
print(spotify.head())

# (E) How Many Records in the Variable "zip Code" are invalid values? 
# That is, they contain letters

# Using regex to identify invalid records in 't_zip Code' variable.
#  (it means that contains letters)
invalid_zipcode = spotify['t_zip Code'].str.contains(r'[a-zA-Z]').sum()
print(f'Total Invalid Zip Code Records: {invalid_zipcode}')
print(f'Total Records: {spotify.shape[0]}')

# (F) Delete records that don't have a valid "zip Code", that is, 
# it contains letters in the values
spotify['t_zip Code'] = spotify['t_zip Code'].astype('unicode')
spotify = spotify[spotify['t_zip Code'].map(lambda x: x.isnumeric())]
spotify.reset_index(drop = True, inplace = True)
print(spotify.shape)
print(spotify.head())

# (G) How many records in the variable "gender" are invalid values? , 
# that is, they contain letters
# Using regex to identify letters in 'v_genero'
invalid_gender = spotify['v_genero'].str.contains(r'[a-zA-Z-ZéüöêåøЧастьХемиуэйЧасть]').sum()
print(f'Total Records With Invalid Gender: {invalid_gender}')
print(f'Total Records: {spotify.shape[0]}')


# (H) Delete the records that don't have a valid "gender",
#  that is, that contain letters in the values
spotify = spotify[~spotify['v_genero'].str.contains(r'[a-zA-Z-ZéüöêåøЧастьХемиуэйЧасть]', na=False)]
print(spotify.shape)
print(spotify.head())


# (I) Clean the variable "name", remove special characters
# and everything must be in lowercase

# This functions just map the column 'name' to keep
#  names even if they have asian characters
import re

def cjk_detect(texts):
    # Korean
    if re.search("[\uac00-\ud7a3]", texts):
        return texts
    # Japanese
    if re.search("[\u3040-\u30ff]", texts):
        return texts
    # Chinese
    if re.search("[\u4e00-\u9FFF]", texts):
        return texts
    else:
        return texts
    
# This functions is used to remove special marks/characters
def remove_punct(text):
    try:
        text=text.replace(".",' ').replace(";",' ').replace(":",' ').replace(",",' ')
        text=text.replace("(",' ').replace(")",' ').replace("|",' ').replace('"',' ')
        text=text.replace("%",' ').replace("$",' ').replace("/",' ').replace('\'',' ')
        text=text.replace("-",' ').replace("_",' ').replace("*",' ').replace('+',' ')
        text=text.replace("#",' ').replace("@",' ').replace("!",' ').replace('?',' ')
        text=text.replace("[",' ').replace("]",' ').replace("'",' ').replace('¡',' ')
    except:
        pass
    return text

# This functions is used to clean 'name' and convert to lowercase
def clean_text(text):
    text=text.lower()
    text=remove_punct(text)
    return text

# Apply 'cjk_detect' function just to return text in its native format
spotify['t_name'] = spotify['t_name'].apply(lambda row: cjk_detect(row))
spotify.reset_index(drop = True, inplace = True)
print(spotify.head())