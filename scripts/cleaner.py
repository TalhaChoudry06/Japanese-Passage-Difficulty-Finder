import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

df = pd.read_csv('data/sentences.csv')
print(df.columns)

df = df.drop_duplicates(subset=['jp_sentence'])\

df.to_csv("cleaned_sentences.csv", index=False)
