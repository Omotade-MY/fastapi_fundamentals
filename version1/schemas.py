from pydantic import BaseModel
import json

class CarInput(BaseModel):
    size: str
    fuel: str = 'electric'
    doors: int
    transmission: str = 'auto'

class TripInput(BaseModel):
    start: int
    end: int
    description: str

class TripOutput(TripInput):
    id: int

class CarOutput(CarInput):
    id: int 
    trips: list[TripOutput] = []


def load_db() -> list[CarOutput]:
    import os
    print(os.getcwd())
    with open('cars.json', 'r') as jsf:
        return [CarOutput.parse_obj(obj) for obj in json.load(jsf)]


def save_db(cars: list[CarInput]):
    with open('cars.json', 'w') as f:
        new_db = [car.dict() for car in cars]
        json.dump(new_db, f, indent=4)

