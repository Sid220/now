import mariadb

conn = mariadb.connect(
    host='127.0.0.1',
    port=3306,
    user='USER',
    password='PASSWORD',
    database='now')

cur = conn.cursor()
