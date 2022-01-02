from typing import Dict, Iterator
from zipfile import ZipFile
from io import BytesIO
from datetime import datetime
from io import TextIOWrapper
import threading
import numpy as np
import httplib2
import csv


# Le mieux pour créer contextes manuellement : avec context lib

class Datapoint :
    def __init__(self, timestamp, consommation):
        self.timestamp = timestamp
        self.consommation = consommation
        
def download_data(h : httplib2.Http ) -> bytes :
    '''
    This function downloads data from RTE url and returns the content as bytes
    '''
    actual_date = datetime.today().strftime('%d/%m/%Y')
    response, content = h.request('https://eco2mix.rte-france.com/curves/eco2mixDl?date={}'.format(actual_date))
    return content
    #déclarer types de sortie

def parse_data(content : bytes) :
    '''
    This function takes as input the data content as bytes, and returns it as a raw list of dictionaries, with every column of the initial file
    '''
    zipfile = ZipFile(BytesIO(content))
    with zipfile.open(zipfile.namelist()[0]) as a_file : 
        spamreader = csv.DictReader(TextIOWrapper(a_file, 'latin-1'), delimiter = '\t')
        return list(spamreader) 

    # sinon changer de structure pour que le zipfile.open ne soit pas à l'intérieur de la fonction, mais plutôt renvoyer un contexte
    # mais mieux de return iterator plutôt que liste
    # mieux pour return une list à partir d'un generator
    # pas besoin d'affecter la variable avant de la return

def into_timestamp(date : str, time : str) :
    '''
    This function converts a date + hours into a timestamp
    '''
    date_time_str = date + " " + time
    date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
    timestamp = int(datetime.timestamp(date_time_obj))
    return timestamp

def conso_datapoint(spamreader : Iterator[Dict]) : # mauvais type est déclaré ! + Ne pas s'engager à ce que ça soit un csv : on peut déclarer itérateur unniquement
    '''
    A generator that takes into argument the raw list and returns a Datapoint with a timestamp and consumption number
    '''
    for row in spamreader :
        if row['Heures']==None or row['Consommation']=='' :
            break
        timestamp = into_timestamp(row['Date'],row['Heures'])
        consommation = int(row['Consommation'])
        yield Datapoint(timestamp,consommation)

def final_dataset(spamreader : csv.DictReader) :
    '''
    This function takes into argument the raw list of dictionaries and returns its data in its final shape
    '''
    gen_datapoint = conso_datapoint(spamreader)
    final_shape =[{'Timestamp' : row.timestamp , 'Consommation' : row.consommation} for row in gen_datapoint]
    return final_shape

    #naviguer uniquement avec ctrl click

def add_table(cursor) :
    '''
    This function creates the RTE_DATA table if it does not exist
    '''
    cursor.execute('''CREATE TABLE IF NOT EXISTS RTE_DATA (
    timestamp1 BIGINT NOT NULL,
    consommation INT,
    PRIMARY KEY (timestamp1));''')

def add_to_db(final, cursor) :
    '''
    This function adds the data in its final shape to the table
    '''
    for dict in final :
        cursor.execute('''INSERT INTO RTE_DATA (timestamp1,consommation)
        SELECT * FROM (SELECT %(Timestamp)s AS timestamp1, %(Consommation)s AS consommation) AS temp
        WHERE NOT EXISTS (
        SELECT timestamp1 FROM RTE_DATA WHERE timestamp1 = %(Timestamp)s) 
        LIMIT 1;''', dict)
        print("success")

def update_db(cursor, h) : 
    '''
    This function concatenates the previous functions
    '''
    add_table(cursor)
    print("hello")
    file = download_data(h)
    dataset_raw = parse_data(file)
    final = final_dataset(dataset_raw)
    add_to_db(final,cursor)
    return None


#formatage de requête sql
#sur 1 serveur, on met base de données
#sur 1 autre, on fait programme Python
#en prod, il y a plusieurs serveurs différents


