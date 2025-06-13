import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

df = pd.read_csv('data/cleaned_sentences.csv')
print(df.columns)

# Randomly sample 200 entries without replacement
sampled_df = df.sample(n=200, random_state=42)  # set random_state for reproducibility

# Save the sampled data to a new CSV
sampled_df.to_csv('sampled_cleaned_sentences.csv', index=False)

print("Sample saved to 'sampled_cleaned_sentences.csv'")

