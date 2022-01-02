from sqlalchemy.orm import Session
from typing import Optional

from . import models


def get_user(db : Session, n : Optional[int] = None):
    data = {}

    if n==None :
        return {'Error' : 'Please specify a value for n'}

    else :
        return db.query(models.Conso_Datapoint).filter(models.Conso_Datapoint.timestamp > user_id)
        cursor.execute(
        SELECT
        FROM_UNIXTIME(timestamp1, '%%Y-%%m-%%dT%%H:%%i') AS date_converted, 
        consommation
        FROM RTE_dATA
        WHERE timestamp1 > UNIX_TIMESTAMP() - %(n)s * 3600
        ORDER BY timestamp1 DESC;, 
        {'n' : n})

        results=cursor.fetchall() # autre méthode pour fetcher au fur et à mesure
        for i in range(len(results)) :
            data[str(results[i]['date_converted'])] = results[i]['consommation']
    
    else :   
        data['Error'] = 'The parameter n is out of range !'

        

    return json.dumps(data)
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()
