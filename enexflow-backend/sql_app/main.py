from typing import Optional, Dict, List

from fastapi import Depends, FastAPI
import httplib2
import crud
from fastapi_utils.tasks import repeat_every
import uvicorn
import MySQLdb
import MySQLdb.connections
from fastapi.middleware.cors import CORSMiddleware
import os

#ensemble des var.env. de l'environnement donné (shell) -> variables définies très haut dans système d'exploitation

origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    mydb = MySQLdb.connect(host='127.0.0.1', user='root', passwd=os.environ['password'], db='rte', charset="utf8") #mettre dans un fichier texte c'est mieux, mais : utiliser variables d'environnement -> valeurs associées à un nom, format clé = valeur. Ex : langue, mdp bdd
    try:
        yield mydb
    finally:
        mydb.close()

h = httplib2.Http()

@app.on_event("startup")
@repeat_every(seconds=15*60, raise_exceptions=True)  #@repeat_every doesn't support dependencies !!
def update():
    mydb = MySQLdb.connect(host='127.0.0.1', user='root', passwd='Crefolet75$', db='rte', charset="utf8")
    crud.update_db(mydb, h)
    mydb.close()

@app.get('/electricity_consumption')
def get_hours(n : Optional[int] = None,  db : MySQLdb.connections.Connection = Depends(get_db)) -> List[Dict[str, str or int]]: 
    data = crud.get_hours(db, n = n)
    return data

@app.get('/refresh_conso')
def update(db : MySQLdb.connections.Connection = Depends(get_db)) -> List[Dict[str, str]]:
    crud.update_db(db, h)
    return [{"state" : "Done fetching data from RTE"}]

if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=5000)
