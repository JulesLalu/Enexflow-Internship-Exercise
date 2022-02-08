# on veut exécuter 2 fonctions asynchrone
# on ne veut pas de fonction app.run qui prenne le contrôle
# serveur web asynchrone, lancer les 2 tâches en parallèle
# framework HTTP qui puisse lancer le code de manière asynchrone
# fonction run qui prenne une coroutine + fonction asyncio qui collecte 2 tâches
# awaitable asyncio.gather(*aws, return_exceptions=False)
# trouver fonction qui lance run de manière asynchrone 

from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import httplib2
import crud
from fastapi_utils.tasks import repeat_every
import uvicorn
import MySQLdb
import MySQLdb.connections
from fastapi.middleware.cors import CORSMiddleware
import json
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
def get_hours(n : Optional[int] = None,  db : MySQLdb.connections.Connection = Depends(get_db)): 
    data = crud.get_hours(db, n = n)
    return data

if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=5000)
