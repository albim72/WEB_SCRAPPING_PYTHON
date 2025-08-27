import mysql.connector

db = mysql.connector.connect(user='root', password='abc123', host='127.0.0.1', port=3306)
cursor = db.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS mojabazax")
db.close()

