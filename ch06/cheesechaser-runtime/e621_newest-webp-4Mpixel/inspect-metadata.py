from tqdm.auto import tqdm
import pandas as pd
tqdm.pandas() # register progress_apply

PARQUET_OLD = './posts-2024-04-07.parquet'
PARQUET_NEW = './table.parquet'

df1 = pd.read_parquet(PARQUET_OLD)
df2 = pd.read_parquet(PARQUET_NEW)

df11 = df1[df1["is_deleted"] == "f"]
df21 = df2[df2["id"] < 5000000]

for row in df11.itertuples():
    print(row.Index)
    print(row)
    break

for row in df21.itertuples():
    print(row.Index)
    print(row)
    break

df3 = pd.DataFrame(data={
    'id': df1["id"].to_list() + df2["id"].to_list(), 
    'tag_string': [x.replace(" ",", ") for x in df1["tag_string"].to_list()] + [", ".join(x) for x in df2["tags"].to_list()], 
})

# Follow the trend.
df3.set_index("id")

df3.to_parquet('./e621-merged.parquet')

print(df3.head(1))
print(df3.tail(1))

print(f"{df3["id"].max()} - {df3.index.max()} - {len(df3.index)}")