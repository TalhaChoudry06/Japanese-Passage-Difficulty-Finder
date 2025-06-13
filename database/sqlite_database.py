import sqlite3
try:

    conn = sqlite3.connect('database/sentences.db')
    cursor = conn.cursor()

    sql = "select sqlite_version();"
    cursor.execute(sql)
    results = cursor.fetchall()
    print(results)

    #adding coloumn level filling with default 0;
    sql = """ALTER TABLE sentences ADD level TEXT DEFAULT '0'"""
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    print ("altering ok")

    #adding coloumn tokens filling with default 0;
    sql = """ALTER TABLE sentences ADD tokens TEXT DEFAULT '0'"""
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    print ("altering ok")

    cursor.close()

except sqlite3.Error as e:
    print ("Error while altering table", e)

finally: 
    if (conn) :
        conn.close()
        print ("connection closed")