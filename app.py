from flask import Flask
from flask_mysqldb import MySQL
from flask import request
import json

app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Crefolet75$'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'rte'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/electricity_consumption/')
def index(): 
    cur = mysql.connection.cursor()

    cur.execute('''SELECT COUNT(*) AS NBROW FROM October30;''')

    results=cur.fetchall()
    size=results[0]['NBROW']-1

    cur.execute('''select id, from_unixtime((conso_date-25568+heures-(1/24))*24*3600, '%Y-%m-%dT%H:%i') as date_converted, consommation
    from October30;''')

    n = int(request.args.get('n'))

    if n>=1 and n<int(size/4)+1 :
        results=cur.fetchall()
        data = {}
        for i in range(4*n-1,-1,-1) :
            data[str(results[size-i]['date_converted'])] = results[size-i]['consommation']

        return json.dumps(data)
    
    else :
        return "The parameter n is out of range !"