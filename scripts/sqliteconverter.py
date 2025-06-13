import pandas as pd
import sqlite3

# Step 1: Load your CSV (make sure it's UTF-8 encoded)
csv_file = 'sampled_cleaned_sentences.csv'  # update this to your actual file path
df = pd.read_csv(csv_file, encoding='utf-8')

# Step 2: Connect to SQLite (this creates a new DB file)
conn = sqlite3.connect('sampled_sentences.db')

# Step 3: Write DataFrame to SQLite
# The table will be named "words" (change as needed)
df.to_sql('sentences', conn, if_exists='replace', index=False)

# Step 4: Done
conn.close()
print("CSV has been successfully converted to SQLite database.")
