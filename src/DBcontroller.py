import constants
import csv
import sqlite3
import time

admins = []
operators = []

def init_admins_and_operators_info():
    global admins, operators
    with open(constants.ADMINSID_PATH, 'r') as fd:
        reader = csv.reader(fd)
        for row in reader:
            admins.append(row[0])
    with open(constants.OPERATORSID_PATH, 'r') as fd:
        reader = csv.reader(fd)
        for row in reader:
            operators.append(row[0])        

def get_admins():
    global admins
    if not admins: # admins is an empty list
        init_admins_and_operators_info()
    return admins


def get_operators():
    global operators
    if not operators: # operators is an empty list
        init_admins_and_operators_info()
    return operators

def create_DBs_if_not_exist():
    # saliva samples submision information DB:
    connection = sqlite3.connect(constants.DB_MEDICALINFO_PATH)
    cursor = connection.cursor()
    cursor.execute( """ CREATE TABLE if not exists muestras_saliva (
                CIP text,
                last_pickup_time text,
                submit_time text,
                time_elapsed text ,
                submission_ID text)
                """)
    connection.commit()
    connection.close()
    # kiosk usage information DB:
    connection = sqlite3.connect(constants.DB_USEINFO_PATH)
    cursor = connection.cursor()
    cursor.execute( """ CREATE TABLE if not exists info_uso (
                ID text,
                event text,
                event_time text)
                """)
    connection.commit()
    connection.close()

def add_new_event(ID, event):
    connection = sqlite3.connect(constants.DB_USEINFO_PATH)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO info_uso VALUES (:ID, :event, :event_time)",
			{
				'ID': ID,
				'event': event,
				'event_time': time.strftime("%m/%d/%Y, %H:%M:%S")
			}) # IMPORTANTE: En internet veras otra forma de hacer el insert mas corta. La puedes hacer pero tendras que mirar como he hecho el codigo del update para ver las adaptaciones que hay que hacer si quieres usar variables o cosas con .get() (como es el caso)
    connection.commit()
    connection.close()

def get_DB_content(DB_name):
    DB_content = ''
    connection = ''
    if DB_name == "muestras_saliva":
        DB_content = "(CIP , Momento recogida kit , Momento deposicion muestra , Tiempo transcurrido , Identificador muestra)\n\n"
        connection = sqlite3.connect(constants.DB_MEDICALINFO_PATH)
    elif DB_name == "info_uso":
        DB_content = "(Identificador o CIP , evento , Fecha y hora evento)\n\n"
        connection = sqlite3.connect(constants.DB_USEINFO_PATH)
    else:
        raise Exception("Has llamado a get_DB_content pasando un nombre de DB distinto a muestras_saliva o info_uso")

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM " + DB_name)

    results = cursor.fetchall()
    for result in results:
        DB_content += str(result) + '\n'

    connection.close()
    return DB_content