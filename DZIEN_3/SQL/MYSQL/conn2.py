#pip install pymysql

import pymysql
cnx = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="passwd")
with cnx.cursor() as cur:
    cur.execute("CREATE DATABASE IF NOT EXISTS mojaBazaX")
cnx.commit(); cnx.close()
