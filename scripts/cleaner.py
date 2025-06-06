import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

df = pd.read_csv('data/merged_clean_n1-n5.csv')
print(df.columns)

print(df["tags"].unique())
df = df.drop_duplicates(subset=['expression'])
df.to_csv("cleaned_data_n1-n5.csv", index=False)
