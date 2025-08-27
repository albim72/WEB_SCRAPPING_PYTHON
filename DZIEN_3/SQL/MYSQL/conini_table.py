import configparser
import mysql.connector

#ładowanie pliki konfiguracyjnego
config = configparser.ConfigParser()
config.read("config.ini")

#pobranie danych z sekcji mysql (config.ini)

db_user = config['mysql']['user']
db_password = config['mysql']['password']
db_host = config['mysql']['host']
db_port = config['mysql']['port']
db_database = config['mysql']['database']

connection = mysql.connector.connect(
    user = db_user,
    password = db_password,
    host = db_host,
    port = db_port,
    database = db_database
)

cursorObject = connection.cursor()
tabela_student = """
CREATE TABLE IF NOT EXISTS student(
firstname varchar(100),
lastname varchar(100),
studentid int primary key
);
"""

cursorObject.execute(tabela_student)

dodaj_studenta = """
INSERT INTO student(firstname,lastname,studentid) values(%s,%s,%s);
"""
val_one = ("Jan","Kot",7674745)
cursorObject.execute(dodaj_studenta,val_one)

val_multi = [
    ("Maria","Wasik",6545363),
    ("Marek","Kowal",654645),
    ("Mat","Kos",57567),
    ("Tomek","Woś",35765),
    ("Leon","Poś",87686754),
    ("Nadia","Ktoś",785676)
]

cursorObject.executemany(dodaj_studenta,val_multi)

connection.commit()

connection.close()
