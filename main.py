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

# Apply 'clean_text' function to convert it to lowercase without affect 
# (Japanese, Chinese & Korean) names
spotify['t_name'] = spotify['t_name'].apply(lambda row: clean_text(row))
spotify.reset_index(drop = True, inplace = True)
print(spotify.head())

# (J) From the variable "artist" select only the 
# first one that appears in the list in addition eliminate special characters
first_artist = spotify['t_artists'].iloc[0]
clean_first_artist = clean_text(first_artist)
clean_first_artist = remove_punct(first_artist)
print(f'No Clean First Artist: {first_artist}')
print(f'Clean First Artist: {clean_first_artist}')


# (K) Normalize the variable "gender" in such a way 
# that you get only 8 categories

# Checking for null values in 'v_genero' variable
spotify['v_genero'].isnull().sum()
spotify['v_genero'].value_counts()
spotify['v_genero'].value_counts(normalize=True)
spotify['v_genero'].value_counts(1)[-4].sum()
spotify['v_genero'].value_counts(1)[-3:].sum()
spotify_genero_norm = dict(zip(list(spotify['v_genero'].value_counts(1)[-17:].index),
                               ['Others']*90))
print(spotify_genero_norm)

# Normalized v_genero variable
spotify['v_genero'].replace(spotify_genero_norm).value_counts()


# (L) Add the following columns to your dataset: zip, lat, lng, city,
# state name using the zips table

# Read 'zips_practica.csv' data table
zips = pd.read_csv('zips_practica.csv')
print(zips.shape)
print(zips.head())

print(zips.dtypes)
print(spotify.dtypes)

zips_subset = zips[['zip','lat','lng','city','state_name']]
print(zips_subset.shape)
print(zips_subset.head())

spotify['t_zip Code'] = spotify['t_zip Code'].astype(str).astype(int)

# Merge spotify & zips_subset dataframes
from pandas.core.reshape.merge import merge
spotify = spotify.merge(zips_subset,right_on = 'zip',left_on = 't_zip Code', how = 'left')
print(spotify.shape)
print(spotify.head())


# (M) Convert the variables "lat" and "lng" into a float type
# and validate data consistency

# Convert 'lat' & 'lng' to float type variables
spotify['lat'] = spotify['lat'].astype(str).astype(float)
spotify['lng'] = spotify['lng'].astype(str).astype(float)
# Verify that 'lat' and 'lng are float type variables' --> consistency
print(spotify.dtypes)
print(spotify['lat'].value_counts())

# Validate 'lat' & 'lng' values
    ## Latitude must be a number between -90 and 90
    ## Longitude must a number between -180 and 180

def lat_val(value):
    if -90<=value<=+90:
        return 'Correct'
    else:
        return 'Incorrect'
    
def lng_val(value):
    if -180<=value<=+180:
        return 'Correct'
    else:
        return 'Incorrect'
    
# This temporal variable is created to validate if 'lat' values are correct
spotify['lat_validation'] = spotify['lat'].apply(lambda row: lat_val(row))
print(spotify.head())

# This temporal variable is created to validate 'lng' values are correct
spotify['lng_validation'] = spotify['lng'].apply(lambda row: lat_val(row))
print(spotify.head())

# Checking 'lat' & 'lng' variables are 'Correct' for all records
print(spotify['lng_validation'].value_counts())

# Checking 'lat' & 'lng' variables are 'Correct' for all records
print(spotify['lat_validation'].value_counts())

# (N) From the variable "city" and "state" remove the digits
# found within the text strings
spotify['city'] = spotify['city'].str.replace(r'[0-9]','')
spotify['state_name'] = spotify['state_name'].str.replace(r'[0-9]','')
print(spotify.shape)
print(spotify.head())

# (O) Create a new variable called "state" that is made up of "city" & "state name"
spotify['state'] = spotify[['city', 'state_name']].agg(', '.join, axis=1)
print(spotify.shape)
print(spotify.head())


# (P) The values of the new variable "state", modify them
# in a certain way that all o them must be in lowercase and without accents

# Convert 'state' column to lowercase
spotify['state'] = spotify['state'].apply(lambda x:x.lower())
print(spotify.head())

# This function is used to delete 'accents' with the 'unicodedata' library
def delete_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

spotify['state'] = spotify['state'].apply(lambda row: delete_accents(row))
print(spotify.head())

print(spotify['d_release_date'].unique())

# (Q) Convert the values in the variable "release date" to type datetime,
# also count those that do not have the necessary structure to be converted
# into datetime and delete those records

# (Q)-I Verify invalid records in 'release_date' 
# (if they have the correct datetime format)
invalid_date = spotify['d_release_date'].str.contains(r'[a-zA-Z]').sum()
print(f'Total Records With Incorrect Structure: {invalid_date}')
print(f'Total Records: {spotify.shape[0]}')

# (Q)-II Convert 'release_date' records to datetime type
spotify['d_release_date'] = pd.to_datetime(spotify['d_release_date'],
                                           format = '%Y-%m-%d %H:%M:%S')
print(spotify.head())
print(spotify.dtypes)