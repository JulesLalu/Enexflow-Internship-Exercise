from sqlalchemy.orm import Session
from typing import Optional, Dict, List
from datetime import datetime
from asyncio.streams import StreamReader
from zipfile import ZipFile
from io import BytesIO
from io import TextIOWrapper
import MySQLdb
import httplib2
import csv
from pypika import Query, Table, Order
import json
import MySQLdb.connections

# Le mieux pour créer contextes manuellement : avec context lib

#fetch last n hours task
rte_data = Table('RTE_DATA')

def get_hours(mydb : MySQLdb.connections.Connection, n : Optional[int] = None) -> Dict:
    '''
    Get the data that was previously imported in the database
    '''
    if n==None :
        return {'Error' : 'Please specify a value for n'}

    else :
        data = {}
        cursor = mydb.cursor()
        query = Query.from_(rte_data).select(
            #datetime.fromtimestamp(rte_data.timestamp1).strftime("%m/%d/%Y, %H:%M:%S"), 
            rte_data.timestamp1,
            rte_data.consommation
            ).where(
                rte_data.timestamp1 > datetime.timestamp(datetime.now()) - n * 3600
            ).orderby(
                rte_data.timestamp1, order = Order.desc
            )
        cursor.execute(str(query))
        mydb.commit()
        cursor.close()
        results=cursor.fetchall() # autre méthode pour fetcher au fur et à mesure
        for i in range(len(results)) :
            data[str(results[i]['date_converted'])] = results[i]['consommation']

        return json.dumps(data)

        # dict1 = db.query(models.Conso_Datapoint.timestamp1, models.Conso_Datapoint.consommation) \
        #     .filter(models.Conso_Datapoint.timestamp1 > datetime.timestamp(datetime.now()) - n * 3600) \
        #     .order_by(models.Conso_Datapoint.timestamp1, desc(models.Conso_Datapoint.timestamp1)) 
        # for key in dict1 :
        #     dict1[key.strftime("%m/%d/%Y, %H:%M:%S")] = dict1.pop(key)
        #     ne pas mettre à jour un dictionnaire : penser programmation fonctionnelle ! Penser en constante plutôt qu'en variable
        # return dict1


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

def create_datapoint(mydb : MySQLdb.connections.Connection, NewRow : Datapoint) -> None:
    cursor = mydb.cursor()
    query = Query.into(rte_data)\
        .insert(NewRow.timestamp, NewRow.consommation)\
        .on_duplicate_key_update(rte_data.consommation, Values(rte_data.consommation))
    cursor.execute(query)
    mydb.commit()
    cursor.close()
    return None

def update_db(db : Session, h : httplib2.Http) -> str :
    file = download_data(h)
    for data_pt in conso_datapoint(file) :
        create_datapoint(db, data_pt)
    return 'db uploaded'

