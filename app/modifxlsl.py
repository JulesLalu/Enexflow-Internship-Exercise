from zipfile import ZipFile
from io import BytesIO
from datetime import datetime
import threading
import numpy as np

def update_db(h, cursor) : 

    actual_date = datetime.today().strftime('%d/%m/%Y')
    response, content = h.request('https://eco2mix.rte-france.com/curves/eco2mixDl?date={}'.format(actual_date))

    zipfile = ZipFile(BytesIO(content))
    l = [[]]

    with zipfile.open(zipfile.namelist()[0]) as a_file : 
        for line in a_file.readlines():
            l.append(line.decode('latin-1').split("\t"))

    del l[0]
    l[0]=['Timestamp', 'Consommation']
    del l[-1]
    i=1
    while l[i][4]!='':
        # suppression des colonnes inutiles
        del l[i][0:2]
        del l[i][3:]
        # passage en timestamp
        date_time_str = l[i][0] + " " + l[i][1]
        date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
        timestamp = datetime.timestamp(date_time_obj)
        del l[i][0]
        l[i][0],l[i][1] = int(timestamp), int(l[i][1])
        # on sort de la boucle si l'excel est rempli jusqu'à 23h45
        if i == len(l)-1 :
            break

        i+=1
    del l[i:]

    np.savetxt("RTE_data.csv",l, delimiter = ', ',fmt ='% s')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS RTE_DATA (
    timestamp1 BIGINT NOT NULL,
    consommation INT,
    PRIMARY KEY (timestamp1));''')

    cursor.execute('''LOAD DATA INFILE 'RTE_data.csv' IGNORE
    INTO TABLE RTE_DATA 
    FIELDS TERMINATED BY ',' 
    LINES TERMINATED BY '\n'
    IGNORE 1 ROWS;''')
    #threading.Timer(15*60, update_db).start()

