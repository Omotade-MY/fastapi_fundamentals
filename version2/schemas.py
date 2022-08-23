from sqlmodel import SQLModel, Field, Relationship

class CarInput(SQLModel):
    size: str
    fuel: str = 'electric'
    doors: int
    transmission: str = 'auto'

class TripInput(SQLModel):
    start: int
    end: int
    description: str

class Trip(TripInput, table=True):
    id: int|None = Field(primary_key=True, default=None)
    car_id: int = Field(foreign_key="car.id")
    car: "Car" = Relationship(back_populates= "trips")

class TripOutput(TripInput):
    id: int

class CarOutput(CarInput):
    id: int 
    trips: list[TripOutput] = []

class Car(CarInput, table=True):
    id: int|None = Field(primary_key=True, default=None)
    trips: list[Trip] = Relationship(back_populates= "car")
