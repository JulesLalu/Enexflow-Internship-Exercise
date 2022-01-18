from sqlalchemy.orm import Session
from typing import Optional, Dict, List
from datetime import datetime
import models
from sqlalchemy.sql.expression import desc
from asyncio.streams import StreamReader
from zipfile import ZipFile
from io import BytesIO
from io import TextIOWrapper
import threading
import numpy as np
import httplib2
import csv
from add_op import Datapoint
from models import Conso_Datapoint

# Le mieux pour créer contextes manuellement : avec context lib

#fetch last n hours task

def get_hours(db : Session, n : Optional[int] = None) -> dict:
    
    if n==None :
        return {'Error' : 'Please specify a value for n'}

    else :
        dict1 = db.query(models.Conso_Datapoint.timestamp1, models.Conso_Datapoint.consommation) \
            .filter(models.Conso_Datapoint.timestamp1 > datetime.timestamp(datetime.now()) - n * 3600) \
            .order_by(models.Conso_Datapoint.timestamp1, desc(models.Conso_Datapoint.timestamp1)) 
        for key in dict1 :
            dict1[key.strftime("%m/%d/%Y, %H:%M:%S")] = dict1.pop(key)
            #ne pas mettre à jour un dictionnaire : penser programmation fonctionnelle ! Penser en constante plutôt qu'en variable
        return dict1


#update db task

class Datapoint :
    def __init__(self, timestamp, consommation):
        self.timestamp : int = timestamp
        self.consommation : int = consommation
        
def context(Bytesfile : bytes) -> StreamReader :
    '''
    This function returns the context to use for parsing the file
    '''
    zipfile = ZipFile(BytesIO(Bytesfile))
    return zipfile.open(zipfile.namelist()[0])

def download_data(h : httplib2.Http ) -> bytes :
    '''
    This function downloads data from RTE url and returns the content as bytes
    '''
    actual_date = datetime.today().strftime('%d/%m/%Y')
    response, content = h.request('https://eco2mix.rte-france.com/curves/eco2mixDl?date={}'.format(actual_date))
    return content

def into_timestamp(date : str, time : str) -> int:
    '''
    This function converts a date + hours into a timestamp
    '''
    date_time_str = date + " " + time
    date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
    timestamp = int(datetime.timestamp(date_time_obj))
    return timestamp

def conso_datapoint(content : bytes) -> Datapoint :
    '''
    A generator that takes into argument the content as bytes and directly returns 
    '''
    with context(content) as a_file :
        spamreader = csv.DictReader(TextIOWrapper(a_file, 'latin-1'), delimiter = '\t')
        for row in spamreader :
            if row['Heures']==None or row['Consommation']=='' :
                break
            timestamp = into_timestamp(row['Date'],row['Heures'])
            consommation = int(row['Consommation'])
            yield Datapoint(timestamp,consommation)

def create_datapoint(db : Session, NewRow : Datapoint) -> Conso_Datapoint:
    exists = db.query(models.Conso_Datapoint.timestamp1).filter_by(timestamp1=NewRow.timestamp).first()  
    #pas besoin si on a déjà la bonne clé primaire -> regarder avec Pypyka     
    if not exists:
        db_datapoint = models.Conso_Datapoint(timestamp1 = NewRow.timestamp, consommation = NewRow.consommation)
        db.add(db_datapoint)
        db.commit()
        db.refresh(db_datapoint)
        return db_datapoint

def update_db(db : Session, h : httplib2.Http) -> str :
    file = download_data(h)
    for data_pt in conso_datapoint(file) :
        create_datapoint(db, data_pt)
    return 'db uploaded'

