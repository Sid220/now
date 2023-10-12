import mariadb

conn = None
cur = None

def db_connect():
    global conn, cur
    conn = mariadb.connect(
    host='127.0.0.1',
    port=3306,
    user='sid',
    password='***REMOVED***',
    database='now')

    cur = conn.cursor()

def db_close():
    print("CLOSED")
    global conn, cur
    cur.close()
    conn.close()
