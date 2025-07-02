import numpy as np
import matplotlib as plt
import pandas as pd 
import sqlite3
import tkinter as tk
from tkinter import ttk
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import joblib
from sklearn.metrics import classification_report, confusion_matrix

def show_dataframe(df):
    root = tk.Tk()
    root.title("DataFrame Viewer")

    frame = ttk.Frame(root)
    frame.pack(expand=True, fill='both')

    xscroll = ttk.Scrollbar(frame, orient='horizontal')
    yscroll = ttk.Scrollbar(frame, orient='vertical')
    tree = ttk.Treeview(frame, columns=list(df.columns), show='headings',
                        xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)

    xscroll.config(command=tree.xview)
    yscroll.config(command=tree.yview)
    xscroll.pack(side='bottom', fill='x')
    yscroll.pack(side='right', fill='y')
    tree.pack(side='left', expand=True, fill='both')

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='center', width=100)

    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))

    root.mainloop()

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Connect and load data 
cnx = sqlite3.connect('database/predicted_sentences.db')
df = pd.read_sql_query("SELECT * FROM sentences_with_predictions", cnx)

# Select features
features = ['n5', 'n4', 'n3', 'n2', 'n1', 'tokens', 'avg_jlpt']
label_column = 'predicted_level'

# Extracting the independent and dependent variables abd showing the dataframe
df_subset = df.iloc[:147143, :]
x = df_subset[features]
y = df_subset[label_column]
# show_dataframe(df_subset)

# Splitting the dataset into the Training set and Test set
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state=0)

# Feature scaling 
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Fitting classifier to the Training set
classifier = LogisticRegression(
    solver = 'newton-cg',
    class_weight = 'balanced'
)
classifier.fit(X_train_scaled, y_train)

# Define easy levels
easy_levels = ['n3', 'n4', 'n5']

# Predict raw
y_pred_raw = classifier.predict(X_test_scaled)

# Group function
def group_labels(label):
    return label if label in easy_levels else 'n2_or_n1'

# Group true and predicted labels
y_test_grouped = [group_labels(label) for label in y_test]
y_pred_grouped = [group_labels(label) for label in y_pred_raw]


print(classification_report(y_test_grouped, y_pred_grouped, zero_division=0))
print(confusion_matrix(y_test_grouped, y_pred_grouped))

# joblib.dump(classifier, 'predicted_sentences_classifier.joblib')
# joblib.dump(scaler, 'predicted_sentences_scaler.joblib')
