import pandas as pd
from pandas import json_normalize

df = pd.read_json("krs.ndjson",lines=True)
print(df)

df_expaned = pd.concat([df.drop(columns=["payload"]),json_normalize(df["payload"])],axis=1)
print(df_expaned)
