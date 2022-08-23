from sqlmodel import SQLModel, Field, Relationship, Column, VARCHAR
from passlib.context import CryptContext

password_context = CryptContext(schemes=['bcrypt'])

class UserOutput(SQLModel):
    id: int
    username: str

class User(SQLModel, table=True):
    id: int|None = Field(primary_key=True, default=None)
    username: str = Field(sa_column=Column("username", VARCHAR, unique=True, index=True))
    password_hash: str = ""

    def set_password(self, password):
        self.password_hash = password_context.hash(password)

    def verify_password(self, password):
        return password_context.verify(password, self.password_hash)


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
