from typing import List

from fastapi import FastAPI, HTTPException
from starlette import status

from models.db import db
from models.models import Sheep

app = FastAPI()

@app.get("/sheep/{id}", response_model=Sheep)
def read_sheep(id: int):
    return db.get_sheep(id)

@app.post("/sheep", response_model=Sheep, status_code=status.HTTP_201_CREATED)
def add_sheep(sheep: Sheep):
    #Check if the Sheep ID already exists to avoid duplicates
    if sheep.id in db.data:
        raise HTTPException(status_code=400, detail="Sheep with this ID already exists")

    # Add the new Sheep to the database
    db.data[sheep.id] = sheep
    return sheep #Return the newly added sheep data

@app.delete("/sheep/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sheep(id: int):
    if id not in db.data:
        raise HTTPException(status_code=404, detail="Sheep with this ID doesn't exist")
    del db.data[id]
    return None

@app.put("/sheep/{id}", response_model=Sheep)
def update_sheep(id: int, sheep: Sheep):
    if id not in db.data:
        raise HTTPException(status_code=404, detail="Sheep with this ID doesn't exist")
    db.data[id] = sheep
    return sheep

@app.get("/", response_model=List[Sheep])
def read_all_sheep():
    return list(db.data.values())

