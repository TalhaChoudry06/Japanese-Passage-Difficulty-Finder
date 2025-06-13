import sys
import sqlite3
import re
import fugashi
import time
from datasets import load_dataset
from tqdm import tqdm

start = time.time()

# Load stopwords dataset
dataset = load_dataset("taishi-i/nagisa_stopwords")
stopwords = dataset["nagisa_stopwords"]["words"]
tagger = fugashi.Tagger()

# Regex (for potential future features, not used here yet)
kanji_re = re.compile(r'[一-龯]')
hiragana_re = re.compile(r'[ぁ-ん]')
katakana_re = re.compile(r'[ァ-ン]')

# Tokenizer function
def tokenize(text):
    return [word.surface for word in tagger(text) if word.surface not in stopwords]

if __name__ == "__main__":
    # Connect to database
    conn = sqlite3.connect("database/sentences.db")
    cursor = conn.cursor()

    # SQLite PRAGMA optimizations
    conn.execute("PRAGMA journal_mode = MEMORY;")       
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA cache_size = 100000;")

    # Create index before updating — only runs if needed
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_jp_id ON sentences(jp_id)")
    conn.commit()

    # Extract and preprocess data
    cursor.execute("SELECT jp_id, jp_sentence FROM sentences")
    rows = cursor.fetchall()

    updates = []
    for row_id, sentence in tqdm(rows, desc="Tokenizing"):
        tokens = len(tokenize(sentence))
        updates.append((tokens, row_id))

    # Batch update
    BATCH_SIZE = 1000
    print("Updating database in batches...")
    conn.execute("BEGIN TRANSACTION")
    for i in tqdm(range(0, len(updates), BATCH_SIZE), desc="Updating DB"):
        batch = updates[i:i + BATCH_SIZE]
        cursor.executemany("UPDATE sentences SET tokens = ? WHERE jp_id = ?", batch)
    conn.commit()

    # Close and report
    print("Batch update took", round(time.time() - start, 2), "seconds")
    print("Completed.")
    conn.close()
