import pandas as pd
import sqlite3
import joblib  # to load saved model and scaler

# --- Load your saved model and scaler ---
# Replace the paths with where you saved your files
classifier = joblib.load('classifier/classifier.joblib')
scaler = joblib.load('classifier/scaler.joblib')

# --- Connect to your database and load full dataset ---
cnx = sqlite3.connect('database/sentences.db')
df_full = pd.read_sql_query("SELECT * FROM sentences", cnx)

# --- Define the features your model expects ---
features = ['n5', 'n4', 'n3', 'n2', 'n1', 'tokens', 'avg_jlpt']

# --- Extract features ---
X_full = df_full[features]

# --- Scale features using the loaded scaler ---
X_full_scaled = scaler.transform(X_full)

# --- Predict raw difficulty levels ---
y_pred_raw = classifier.predict(X_full_scaled)

# Apply grouping logic
easy_levels = ['n3', 'n4', 'n5']
y_pred = [label if label in easy_levels else 'n2_or_n1' for label in y_pred_raw]

# Add predictions back to DataFrame (overwrite 'label' column)
df_full['label'] = y_pred  # <- overwrite existing 'label' column in df

# Connect to your existing SQLite database
cnx = sqlite3.connect('database/sentences.db')
cursor = cnx.cursor()

# Update 'label' column in the database row-by-row
for _, row in df_full.iterrows():
    sql = "UPDATE sentences SET level = ? WHERE jp_id = ?"
    cursor.execute(sql, (row['level'], row['jp_id']))


cnx.commit()
cnx.close()

print("Existing 'level' column updated in the database.")
