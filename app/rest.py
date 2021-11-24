import pymysql
from app import app
from db import mysql
from flask import json
from flask import request

@app.route('/electricity_consumption/')
def index(): 
    conn = mysql.connect()

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    data = {}
    rq=request.args.get('n')
    try :
        n = int(rq)

        if n>=1 :

            cursor.execute('''
            SELECT
            FROM_UNIXTIME(timestamp1, '%%Y-%%m-%%dT%%H:%%i') AS date_converted, 
            consommation
            FROM RTE_dATA
            WHERE timestamp1 > UNIX_TIMESTAMP() - %(n)s * 3600
            ORDER BY timestamp1 DESC;''', 
            {'n' : n})

            results=cursor.fetchall()
            for i in range(len(results)) :
                data[str(results[i]['date_converted'])] = results[i]['consommation']
        
        else :   
            data['Error'] = 'The parameter n is out of range !'

    except Exception as e:
        if rq==None :
            data['Error'] = 'Please specify a value for n'

    return json.dumps(data)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')