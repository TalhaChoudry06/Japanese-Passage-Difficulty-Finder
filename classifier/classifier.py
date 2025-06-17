import numpy as np
import matplotlib as plt
import pandas as pd 
import sqlite3
import tkinter as tk
from tkinter import ttk

def show_dataframe(df):
    root = tk.Tk()
    root.title("DataFrame Viewer")

    frame = ttk.Frame(root)
    frame.pack(expand=True, fill='both')

    # Scrollbars
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

cnx = sqlite3.connect('database/sampled_sentences.db')

df = pd.read_sql_query("SELECT * FROM sentences", cnx)
df_subset = df.iloc[:5, :]
show_dataframe(df_subset)
