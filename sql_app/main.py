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
import crud, models
from database import SessionLocal, engine
import json
from fastapi_utils.tasks import repeat_every
import uvicorn

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

h = httplib2.Http()

@app.on_event("startup")
@repeat_every(seconds=15 * 60)
def update(db : Session = Depends(get_db)):
    return crud.update_db(db, h)


@app.get('/electricity_consumption/')
def get_hours(n : Optional[int] = None,  db : Session = Depends(get_db)): 
    data = crud.get_hours(db, n = n)
    return data

if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=5000)
