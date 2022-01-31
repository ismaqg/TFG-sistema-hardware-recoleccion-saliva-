from Person import ActivePerson
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
				'event_time': time.strftime("%d/%m/%Y, %H:%M:%S")
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


# the function raises an exception if the current person using the system is not an user
# returns false if:
#    - it's the first time that the user uses the system
#    - the last register of the user says that he/she has submited a sample (which means that he/she hasn't a kit now)
# returns true if:
#    - the last register of the user says that he/she hasn't submited a sample (which means that he/she has a kit now)
# Note: returning true doesn't disable the option of collecting another kit (because the user maybe lost his kit)
def user_has_kit():
    if ActivePerson.getCurrent().get_status() != "USER":
        raise Exception("Current person using the system is not an user, it's a " + ActivePerson.getCurrent().get_status() + " so there is not information about if 'user has kit'")
    else:
        connection = sqlite3.connect(constants.DB_MEDICALINFO_PATH)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM muestras_saliva WHERE CIP = '" + ActivePerson.getCurrent().get_CIP() + "' ORDER BY oid DESC") # the last row of a certain user is the one with the highest oid (and the cip of that user). This is why I order descending and only get the first row after ordering
        last_register_of_that_user = cursor.fetchone()
        connection.close()
        if last_register_of_that_user == None:
            return False
        else:
            if last_register_of_that_user[2] == "NO SUBMISSION": # the column [2] has the information about the last submission moment
                return True  # note that the fact that a row of one user exists, means that he/she requested a kit.
            else: # the last interection of the user with the system was to submit a sample, so the user has not a kit.
                return False 