import constants
import csv
import sqlite3

def get_admins():
    admins = []
    with open(constants.ADMINSID_PATH, 'r') as fd:
        reader = csv.reader(fd)
        for row in reader:
            admins.append(row[0])
    return admins

def get_operators():
    operators = []
    with open(constants.OPERATORSID_PATH, 'r') as fd:
        reader = csv.reader(fd)
        for row in reader:
            operators.append(row[0])
    return operators

def create_DBs_if_not_exist():
    # saliva samples submision information DB:
    connection = sqlite3.connect(constants.DB_MEDICALINFO_PATH)
    cursor = connection.cursor()
    cursor.execute( """ CREATE TABLE if not exists muestras_saliva (
                CIP text,
                last_pickup_date text,
                submit_date text,
                time_elapsed text ,
                submission_ID text)
                """)
    connection.commit()
    connection.close()
    # kiok usage information DB:
    connection = sqlite3.connect(constants.DB_MEDICALINFO_PATH)
    cursor = connection.cursor()
    cursor.execute( """ CREATE TABLE if not exists info_uso (
                ID_barcode text,
                event text,
                event_date text)
                """)
    connection.commit()
    connection.close()