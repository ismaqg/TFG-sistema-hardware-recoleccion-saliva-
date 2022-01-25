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

def create_DB_if_not_exists():
    connection = sqlite3.connect(constants.DB_PATH)
    cursor = connection.cursor()
    cursor.execute( """ CREATE TABLE if not exists registro (
                CIP text,
                acess_date text,
                kit_pick integer,
                submit_ID text ,
                submit_date text)
                """)
    connection.commit()
    connection.close()