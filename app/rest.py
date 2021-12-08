import pymysql
import httplib2
from app import app
import modifxlsl
from db import mysql
from flask import json
from flask import request
import cryptography


h = httplib2.Http('.cache')

conn = mysql.connect()
cursor = conn.cursor(pymysql.cursors.DictCursor)

modifxlsl.update_db(h, cursor)

@app.route('/electricity_consumption/')
def index(): 
    
    data = {}
    rq=request.args.get('n')

    try :
        n = int(rq)
    except TypeError :
        return {'Error' : 'Please specify a value for n'}
    except ValueError :
        return {'Error' : 'n must be an integer'}

    if n>=1 :

        cursor.execute('''
        SELECT
        FROM_UNIXTIME(timestamp1, '%%Y-%%m-%%dT%%H:%%i') AS date_converted, 
        consommation
        FROM RTE_dATA
        WHERE timestamp1 > UNIX_TIMESTAMP() - %(n)s * 3600
        ORDER BY timestamp1 DESC;''', 
        {'n' : n})

        results=cursor.fetchall() # autre méthode pour fetcher au fur et à mesure
        for i in range(len(results)) :
            data[str(results[i]['date_converted'])] = results[i]['consommation']
    
    else :   
        data['Error'] = 'The parameter n is out of range !'

        

    return json.dumps(data)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')