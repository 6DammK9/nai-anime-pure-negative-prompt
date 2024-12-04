# install necessary packages, you can choose pyarrow or fastparquet
#%pip install pandas pyarrow

from tqdm.auto import tqdm
import pandas as pd
tqdm.pandas() # register progress_apply

# read parquet file
df = pd.read_parquet('./metadata.parquet')
print(df.head()) # check the first 5 rows

#print(df.columns) # you can check the columns of the dataframe
necessary_rows = [
    "created_at", "score", "rating", "tag_string", "up_score", 
    "down_score", "fav_count"
]
df = df[necessary_rows] # shrink the dataframe to only necessary columns
df['created_at'] = pd.to_datetime(df['created_at']) # convert to datetime

datetime_start = pd.Timestamp('2007-01-01', tz='UTC')
datetime_end = pd.Timestamp('2008-01-01', tz='UTC')
subdf = df[(df['created_at'] >= datetime_start) & 
           (df['created_at'] < datetime_end)]

# count some rating
print(subdf['rating'].value_counts())
# export subdataframe
subdf.to_parquet('./metadata-2007.parquet')