import configparser
import pymysql

#ładowanie pliki konfiguracyjnego
config = configparser.ConfigParser()
config.read("config.ini")

#pobranie danych z sekcji mysql (config.ini)

db_user = config['mysql']['user']
db_password = config['mysql']['password']
db_host = config['mysql']['host']
db_port = int(config['mysql']['port'])
db_database = config['mysql']['database']

connection = pymysql.connect(
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port,
    database=db_database
)

cursorObject = connection.cursor()
query = 'SELECT firstname,lastname FROM student;'
cursorObject.execute(query)
print(cursorObject)

wynik = cursorObject.fetchall()
print(type(wynik))

for x,y in wynik:
    print(f"imię: {x}, nazwisko: {y}")
print("_"*50)

query2 = 'SELECT firstname,lastname FROM student WHERE studentid > 750600;'

cursorObject.execute(query2)
print(cursorObject)

wynik = cursorObject.fetchall()
print(type(wynik))

for x,y in wynik:
    print(f"imię: {x}, nazwisko: {y}")
print("_"*50)

query3 = 'SELECT * FROM vstud;'

cursorObject.execute(query3)
print(cursorObject)

wynik = cursorObject.fetchall()
print(type(wynik))

for x,y in wynik:
    print(f"nazwisko: {y}, id: {x}")
print("_"*50)
