from Person import ActivePerson
import Screen_manager
import constants
import Arduino_controller
import Counters

import csv
import sqlite3
import time
from datetime import datetime
import psycopg2



admins = []
operators = []
operators_emails = []

def init_admins_and_operators_info():
    global admins, operators, operators_emails
    with open(constants.ADMINSID_PATH, 'r') as fd:
        reader = csv.reader(fd)
        for row in reader:
            admins.append(row[0])
    with open(constants.OPERATORSID_PATH, 'r') as fd:
        reader = csv.reader(fd)
        for row in reader:
            operators.append(row[0])
    with open(constants.OPERATORS_EMAILS_PATH, 'r') as fd:
        reader = csv.reader(fd)
        for row in reader:
            operators_emails.append(row[0])

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

def get_operators_emails():
    global operators_emails
    if not operators_emails: # operators_emails is an empty list
        init_admins_and_operators_info()
    return operators_emails



# returns, in this order: available_kits, stored_samples and available_labels
def read_available_resources_csv():
    with open(constants.AVAILABLE_RESOURCES_AND_INFO_PATH, 'r') as fd:
        data = list(csv.reader(fd))
    return [ int(data[0][1]), int(data[1][1]), int(data[2][1]) ]

def read_container_number_csv():
    with open(constants.AVAILABLE_RESOURCES_AND_INFO_PATH, 'r') as fd:
        data = list(csv.reader(fd))
    return int(data[3][1])  # the container number is in the fourth line, second column of the csv.


def write_available_resources_csv(available_kits, stored_samples, available_labels):
    #I think that there is no option to write a specific row (giving the index) in a csv with python, so I will read the entire content of the csv and rewrite it:
    container_number = read_container_number_csv()
    data = [
        ['available_kits', available_kits],
        ['stored_samples', stored_samples],
        ['available_labels', available_labels],
        ['container_number', container_number]  ]
    __write_csv(constants.AVAILABLE_RESOURCES_AND_INFO_PATH, data)

def write_container_number_csv(container_number):
    #I think that there is no option to write a specific row (giving the index) in a csv with python, so I will read the entire content of the csv and rewrite it:
    available_kits, stored_samples, available_labels = read_available_resources_csv()
    data = [
        ['available_kits', available_kits],
        ['stored_samples', stored_samples],
        ['available_labels', available_labels],
        ['container_number', container_number]  ]
    __write_csv(constants.AVAILABLE_RESOURCES_AND_INFO_PATH, data)

def __write_csv(path, data):
    with open(path, 'w') as fd:
        writer = csv.writer(fd)
        writer.writerows(data)



def get_messages(language_file_path):
    messages = []
    with open(language_file_path, 'r') as fd:
        reader = csv.reader(fd, delimiter=';')  # my csv is using ';' as delimiter, but if no delimiter is speficied, python think that ',' is also a valid delimiter (which, in this csv, will make the program to work abnormally because I'm using ',' in the middle of some rows). This is why we need to specify that ';' is the only valid separator/delimiter
        for row in reader:
            messages.append(row[0].replace('\\n', '\n'))  # the 'replace' is because \n in the csv is stored as \\n
    return messages



def create_DBs_if_not_exist():
    # saliva samples submision information DB:
    connection = sqlite3.connect(constants.DB_MEDICALINFO_PATH)
    cursor = connection.cursor()
    cursor.execute( """ CREATE TABLE if not exists muestras_saliva (
                CIP text,
                last_pickup_time text,
                submit_time text,
                time_elapsed text ,
                submission_ID text,
                valid text,
                min_temperature real,
                max_temperature real )
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
    # remote DB:
    conn = psycopg2.connect(
        host= "ec2-54-220-243-77.eu-west-1.compute.amazonaws.com",
        database= "d8s1tilci8353n",
        user= "vbfblvogizjcup",
        password= "2adc81cd9aaa58f02c6591e49b859d41428a23e1ebcd511e00a1450c54f25c71")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE if not exists muestras_saliva (
                CIP text,
                last_pickup_time text,
                submit_time text,
                time_elapsed text,
                submission_ID text PRIMARY KEY,
                valid text,
                min_temperature real,
                max_temperature real,
                container_ID text )
                """)
    cursor.close()
    conn.commit()
    conn.close()

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

def get_local_DB_content(DB_name):
    DB_content = ''
    connection = None
    if DB_name == "muestras_saliva":
        DB_content = "(CIP , Momento recogida kit , Momento deposicion muestra , Tiempo transcurrido , Identificador muestra , Válida?, Mínima temperatura, Máxima temperatura)\n\n"
        connection = sqlite3.connect(constants.DB_MEDICALINFO_PATH)
    elif DB_name == "info_uso":
        DB_content = "(Identificador o CIP , evento , Fecha y hora evento)\n\n"
        connection = sqlite3.connect(constants.DB_USEINFO_PATH)
    else:
        Screen_manager.get_root().destroy()
        raise Exception("Has llamado a get_local_DB_content pasando un nombre de DB distinto a muestras_saliva o info_uso")

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM " + DB_name)

    results = cursor.fetchall()
    for result in results:
        DB_content += str(result) + '\n'

    connection.close()
    return DB_content


# Basically: the functions returns if there is a record with kitpick information and without submit information
# the function raises an exception if the current person using the system is not an user
# returns false if:
#    - it's the first time that the user uses the system
#    - the last register of the user says that he/she has submited a sample (which means that he/she hasn't a kit now)
# returns true if:
#    - the last register of the user says that he/she hasn't submited a sample (which means that he/she has a kit now)
# Note: returning true doesn't disable the option of collecting another kit (because the user maybe lost his kit)
def user_has_kit():
    # TODO: He cambiado las cosas que cogia en el select (ahora ya no cojo el oid). Si esta funcion peta es que hace falta coger también el oid si luego hago un order by oid
    if ActivePerson.getCurrent().get_status() != "USER":
        Screen_manager.get_root().destroy()
        raise Exception("Current person using the system is not an user, it's a " + ActivePerson.getCurrent().get_status() + " so there is not information about if 'user has kit'")
    else:
        connection = sqlite3.connect(constants.DB_MEDICALINFO_PATH)
        cursor = connection.cursor()
        cursor.execute("SELECT submit_time FROM muestras_saliva WHERE CIP = '" + ActivePerson.getCurrent().get_CIP() + "' ORDER BY oid DESC") # the last row of a certain user is the one with the highest oid (and the cip of that user). This is why I order descending and only get the first row after ordering
        last_submission_of_that_user = cursor.fetchone() 
        connection.close()
        if last_submission_of_that_user == None:
            return False
        else:
            if last_submission_of_that_user[0] == "NO SUBMISSION": # [0] because the fetchone returns a tuple (in this case of one element, look at the SELECT executed) and we want that element. We cannot do directly cursor.fetchone()[0] some lines above because maybe cursor.fetchone() equals to 'None'
                return True  # note that the fact that a row of one user exists, means that he/she requested a kit.
            else: # the last interection of the user with the system was to submit a sample, so the user has not a kit.
                return False


# PRE: The user has kit (i.e. the is a record of that user with kitpick information and without submit information)
def update_time_pickup_kit():
    if not user_has_kit():
        Screen_manager.get_root().destroy()
        raise Exception("PRE of update_time_pickup_kit is not satisfied")
    connection = sqlite3.connect(constants.DB_MEDICALINFO_PATH)
    cursor = connection.cursor()
    # get the oid (primary key) of the last record (which is the record with kitpick info but not submit info) of the current user:
    cursor.execute("SELECT oid FROM muestras_saliva WHERE CIP = '" + ActivePerson.getCurrent().get_CIP() + "' ORDER BY oid DESC")
    oid = cursor.fetchone()[0]  # [0] because we want only the integer contained in the tuple of one element that cursor.fetchone() is returning   
    # update that record:  
    cursor.execute("UPDATE muestras_saliva SET " +
                 "last_pickup_time = '" + time.strftime("%d/%m/%Y, %H:%M:%S") + "' " +
                 "WHERE oid = '" + str(oid) + "' ")  # str(oid) because oid variable is integer! (tested)
    connection.commit()
    connection.close() 


# add new record to the medical info DB. A new record is created when the user, without a kit, wants a new kit. And is created with the kitpick information only (and will be completed with the sample deposition when the user submits a sample)
# PRE: The user has NOT a kit (i.e. there is not a record of that user with kitpick information and without submit information)
# NOTE: The submission time will be completed as "NO SUBMISSION"
def add_new_record_with_pickup_kit():
    if user_has_kit():
        Screen_manager.get_root().destroy()
        raise Exception("PRE of add_new_record_with_pickup_kit is not satisfied")
    connection = sqlite3.connect(constants.DB_MEDICALINFO_PATH)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO muestras_saliva VALUES (:CIP, :last_pickup_time, :submit_time, :time_elapsed, :submission_ID, :valid, :min_temperature, :max_temperature)",
                    {
                        'CIP': ActivePerson.getCurrent().get_CIP(),
                        'last_pickup_time': time.strftime("%d/%m/%Y, %H:%M:%S"),
                        'submit_time': "NO SUBMISSION",
                        'time_elapsed': "-",
                        'submission_ID': "-",
                        'valid': "-",
                        'min_temperature': -100.0,  # TODO: Igual no se lo traga así y hay que ponerlo como string
                        'max_temperature': 100.0
                    })
    connection.commit()
    connection.close()


# PRE: The user has a kit (if not, it's impossible to submit a sample!)
def add_sample_submission():
    if not user_has_kit():
        Screen_manager.get_root().destroy()
        raise Exception("PRE of add_sample_submission is not satisfied")
    connection = sqlite3.connect(constants.DB_MEDICALINFO_PATH)
    cursor = connection.cursor()
    # get the oid (primary key) of the last record (which is the record with kitpick info but not submit info) of the current user:
    cursor.execute("SELECT oid, last_pickup_time FROM muestras_saliva WHERE CIP = '" + ActivePerson.getCurrent().get_CIP() + "' ORDER BY oid DESC")
    query_result = cursor.fetchone()  # touple of 2 elements: oid and last_pickup_time
    oid = query_result[0]
    claim_kit_time = query_result[1]
    submit_time = time.strftime("%d/%m/%Y, %H:%M:%S") 
    min_T = max_T = Arduino_controller.get_deposit_temperature()  # TODO: Creo que sería mejor que se pudiesen llamar tal cual a las funciones de Arduino_controller (tal como estoy haciendo aquí, sin ver si está vivo o no) y que se hiciese allí dentro toda la gestión que hay que hacer si arduino está inoperativo
    valid = "NO"
    if min_T >= str(constants.MIN_ALLOWED_TEMPERATURE) and max_T <= str(constants.MAX_ALLOWED_TEMPERATURE):
            valid = "YES"
    # update that record with submission info:  
    cursor.execute("UPDATE muestras_saliva SET " +
                 "submit_time = '" + submit_time + "', " +
                 "time_elapsed = '" + str( datetime.strptime(submit_time, "%d/%m/%Y, %H:%M:%S") - datetime.strptime(claim_kit_time, "%d/%m/%Y, %H:%M:%S") ) + "', " +  # "%d/%m/%Y, %H:%M:%S" indicates the format that the submit_time and claim_kit_time variables have.
                 "valid = '" + valid + "', " +
                 "min_temperature = '" + min_T + "', " +
                 "max_temperature = '" + max_T + "' " +
                 "WHERE oid = '" + str(oid) + "' ")
    connection.commit()
    connection.close()

# PRE: The user has a kit
def add_submission_ID(submissionID):
    if not user_has_kit():
        Screen_manager.get_root().destroy()
        raise Exception("PRE of add_submission_ID is not satisfied")
    connection = sqlite3.connect(constants.DB_MEDICALINFO_PATH)
    cursor = connection.cursor()
    # get the oid (primary key) of the last record (which is the record with kitpick info but not submit info) of the current user:
    cursor.execute("SELECT oid FROM muestras_saliva WHERE CIP = '" + ActivePerson.getCurrent().get_CIP() + "' ORDER BY oid DESC")
    oid = cursor.fetchone()[0]  # [0] because we want only the integer contained in the tuple of one element that cursor.fetchone() is returning
    # update that record:  
    cursor.execute("UPDATE muestras_saliva SET " +
                 "submission_ID = '" + submissionID + "' " +
                 "WHERE oid = '" + str(oid) + "' ")  # str(oid) because oid variable is integer! (tested)
    connection.commit()
    connection.close()


def modify_DB_with_new_temperature(T):
    # TODO: Aqui hay que mirar la temperatura min y max que había por cada fila (en la que hubiesen submissions). if T < min_T: min_T = T; elif T > max_T: max_T = T. Y si T se sale de los margenes de seguridad: Valid = "NO" 
    pass
    


def insert_local_DB_sample_submissions_into_remote_DB_and_delete_local_DB_sample_submissions():
    # Take the content of the local DB:
    connection = sqlite3.connect(constants.DB_MEDICALINFO_PATH)
    cursor = connection.cursor()
    # Select (in the local DB) the rows that contain the information of the samples submitted and store them in a variable:
    cursor.execute("SELECT * FROM muestras_saliva WHERE submit_time <> 'NO SUBMISSION'") 
    local_DB_submissions = cursor.fetchall()
    # Add to the selected rows a new column: container_ID:
    container_ID = constants.MACHINE_ID + str(Counters.get_container_number())  # The concatenation of machine_ID plus the container number is the identification of a certain cointainer, printed in a label in the moment that an operator/admin collects the samples container
    samples_collected = []
    for row in local_DB_submissions:
        samples_collected.append(row + (container_ID,))  # add to each row a new element that is the container ID (casted to tuple of one element, to be added to the row, which is a tuple of many elements). That tuple will be a new element of the samples_collected list, ready to be added in the remote DB
    cursor.close()
    connection.close()
    # Insert those rows in the remote DB:
    conn = psycopg2.connect(
        host= "ec2-54-220-243-77.eu-west-1.compute.amazonaws.com",
        database= "d8s1tilci8353n",
        user= "vbfblvogizjcup",
        password= "2adc81cd9aaa58f02c6591e49b859d41428a23e1ebcd511e00a1450c54f25c71")
    cursor = conn.cursor()
    query = "INSERT INTO muestras_saliva (CIP, last_pickup_time, submit_time, time_elapsed, submission_ID, valid, min_temperature, max_temperature, container_ID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(query, samples_collected)
    cursor.close()
    conn.commit()
    conn.close()
    # Delete local DB sample sumbissions:
    connection = sqlite3.connect(constants.DB_MEDICALINFO_PATH)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM muestras_saliva WHERE submit_time <> 'NO SUBMISSION'")
    connection.commit()
    connection.close()
     


# TODO: eliminar la existencia de la tabla local porque si no no concuerda con la cantidad de columnas que contemplo ahora + funciones para toquetear esos campos nuevos (como modify_DB_with_new_temperature(T)) + DB remota para info_uso también (opcional. Hacerlo mucho mas adelante si sobra tiempo)


"""
IMPORTANTE:
Es necesaria una BD local (que luego se pasa a la remota) por varios motivos:
1- Por narices hay que guardar en algun lado lo que tengo almacenado en la maquina para actualizar su temperatura. Lo mismo para el ID del contenedor. Ya que almaceno eso pues aprovecho y lo pongo todo y luego solamente un insert de todo de golpe en la remota
2- Hay que almacenar en local todos los kits cogidos sin sample devuelto, ya que eso en lo remoto no sirve de na
"""