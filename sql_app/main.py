# on veut exécuter 2 fonctions asynchrone
# on ne veut pas de fonction app.run qui prenne le contrôle
# serveur web asynchrone, lancer les 2 tâches en parallèle
# framework HTTP qui puisse lancer le code de manière asynchrone
# fonction run qui prenne une coroutine + fonction asyncio qui collecte 2 tâches
# awaitable asyncio.gather(*aws, return_exceptions=False)
# trouver fonction qui lance run de manière asynchrone 

'''
h : httplib2.Http = httplib2.Http('.cache')

conn = mysql.connect()
cursor = conn.cursor(pymysql.cursors.DictCursor)
 
def periodic(period):
    def scheduler(fcn):

        async def wrapper(*args, **kwargs):

            while True:
                asyncio.create_task(fcn(*args, **kwargs))
                await asyncio.sleep(period)

        return wrapper

    return scheduler

@periodic(15*60)
async def update(*args, **kwargs):
    update_db(*args,**kwargs)
'''

'''
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

'''

if __name__ == '__main__':
    app.run()
    print("coucou")
    asyncio.run(update(cursor,h))

