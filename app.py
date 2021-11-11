from flask import Flask
from flask_mysqldb import MySQL
from flask import request
import json

app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'rte'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/electricity_consumption/')
def index(): 
    cur = mysql.connection.cursor()

    cur.execute('''
    SELECT COUNT(*) AS NBROW 
    FROM October30;''')

    results=cur.fetchall()
    size=results[0]['NBROW']-1
    
    data = {}

    try :
        param = request.args.get('n')

        cur.execute('''
        SELECT
        FROM_UNIXTIME(timestamp, '%Y-%m-%dT%H:%i') AS date_converted, 
        consommation
        FROM October30
        WHERE timestamp > UNIX_TIMESTAMP() - %n * 3600
        ORDER BY timestamp DESC;''', 
        {'n' : param})

        n=int(param)
        if n>=1 and n<int(size/4)+2 :
            results=cur.fetchall()
            for i in range(4*n-1,-1,-1) :
                data[str(results[size-i]['date_converted'])] = results[size-i]['consommation']
        
        else :   
            data['Error'] = 'The parameter n is out of range !'

    except request.args.get('n')==None:
            data['Error'] = 'Please specify a value for n'

    return json.dumps(data)