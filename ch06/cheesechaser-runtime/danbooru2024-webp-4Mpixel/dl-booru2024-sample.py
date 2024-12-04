#%pip install cheesechaser # >=0.2.0
from cheesechaser.datapool import Danbooru2024WebpDataPool
from cheesechaser.query import DanbooruIdQuery

pool = Danbooru2024WebpDataPool()
#my_waifu_ids = DanbooruIdQuery(['surtr_(arknights)', 'solo']) 
# above is only available when Danbooru is accessible, if not, use following:
import pandas as pd

# read parquet file
df = pd.read_parquet('metadata.parquet', 
                     columns=['id', 'tag_string']) # read only necessary columns
                     
#surtr_(arknights) -> 'surtr_\\(arknights\\)'
#It gets interpreted as regex so we need to escape the brackets
subdf = df[df['tag_string'].str.contains('astolfo_\\(fate\\)') &
           df['tag_string'].str.contains('solo')]
ids = subdf.index.tolist()

SAMPLE_SIZE = 100

print(ids[:SAMPLE_SIZE]) # check the first 100 ids

# download danbooru images with surtr+solo, to directory /data/exp2_surtr

# 241203: Limit to 100 images here.

pool.batch_download_to_directory(
    resource_ids=ids[:SAMPLE_SIZE],
    dst_dir='./data/exp2_surtr',
    max_workers=4,
)