import sys
import sqlite3
import re
import fugashi
import time
from datasets import load_dataset
from tqdm import tqdm

start = time.time()

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
    cursor.execute("SELECT jp_id, n5, n4, n3, n2, n1 FROM sentences")
    rows = cursor.fetchall()

    updates = []
    for row in tqdm(rows, desc="Computing avg_jlpt"):
        jp_id, n5, n4, n3, n2, n1 = row
        total = n1 + n2 + n3 + n4 + n5
        if total > 0:
            avg_jlpt = (n5*5 + n4*4 + n3*3 + n2*2 + n1*1) / total
        else:
            avg_jlpt = 5
        updates.append((avg_jlpt, jp_id))

    # Batch update
    BATCH_SIZE = 1000
    print("Updating database in batches...")
    conn.execute("BEGIN TRANSACTION")
    for i in tqdm(range(0, len(updates), BATCH_SIZE), desc="Updating DB"):
        batch = updates[i:i + BATCH_SIZE]
        cursor.executemany("UPDATE sentences SET avg_jlpt = ? WHERE jp_id = ?", batch)
    conn.commit()

    # Close and report
    print("Batch update took", round(time.time() - start, 2), "seconds")
    print("Completed.")
    conn.close()
