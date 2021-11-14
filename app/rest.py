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

    try :
        n = int(request.args.get('n'))

        if n>=1 :

            cursor.execute('''
            SELECT
            FROM_UNIXTIME(timestamp, '%Y-%m-%dT%H:%i') AS date_converted, 
            consommation
            FROM October30
            WHERE timestamp > UNIX_TIMESTAMP() - %n * 3600
            ORDER BY timestamp DESC;''', 
            {'n' : n})

            results=cursor.fetchall()
            for i in range(len(results[:][0])) :
                data[str(results[i]['timestamp'])] = results[i]['consommation']
        
        else :   
            data['Error'] = 'The parameter n is out of range !'

    except request.args.get('n')==None:
            data['Error'] = 'Please specify a value for n'

    return json.dumps(data)