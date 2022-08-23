from fastapi import HTTPException, Depends, APIRouter
from routers.auth import get_current_user
from schemas import CarOutput, TripInput, CarInput, Car, Trip, User
from sqlmodel import Session, select
from db import engine, get_session


router = APIRouter(prefix="/api/cars")

@router.get("/")
def get_cars(size: str|None = None, doors: int|None = None, session: Session = Depends(get_session)) -> list:
    
    query = select(Car)
    if size:
        query = query.where(Car.size == size)
    if doors:
        query = query.where(Car.doors >= doors)

    result = session.exec(query).all()
    return result 

@router.get("/{id}", response_model=CarOutput)
def get_cars_id(id:int, session: Session = Depends(get_session)) -> dict:
    car = session.get(Car, id)
    if car:
        return car
    else:
        raise HTTPException(status_code=404, detail=f"No such car with id {id}")
    
@router.post("/", response_model=Car)
def add_car(car_input: CarInput, session: Session = Depends(get_session),
                        user: User = Depends(get_current_user)) -> Car:
     
    new_car = Car.from_orm(car_input)
    session.add(new_car)
    session.commit()
    session.refresh(new_car)
    return new_car


@router.delete("/{id}", status_code= 200)
def remove_car(id: int, session: Session = Depends(get_session)):
    car = session.get(Car, id)
    if car:
        session.delete(car)
        session.commit()

    else:
        raise HTTPException(status_code=404, detail=f"No such car with id {id}")


@router.put("/{id}", response_model=CarOutput)
def change_car(id: int, car_input: CarInput, session: Session = Depends(get_session)) -> Car:
    car = session.get(Car, id)
    if car:
        new_car = Car.from_orm(car_input)
        car.size = new_car.size
        car.doors = new_car.doors
        car.transmission = new_car.transmission
        car.fuel = new_car.fuel

        session.commit()

        return car
         
    else:
        raise HTTPException(status_code=404, detail=f"No such car with id {id}")

@router.post("/{id}/trips", response_model=TripInput)
def add_trip(car_id: int, trip_input: TripInput, session: Session = Depends(get_session)) -> Trip:
    car = session.get(Car, car_id)
    if car:
        trip = Trip(start = trip_input.start, end= trip_input.end, description=trip_input.description,
        car= car, car_id=car_id)
        #Trip.from_orm(trip_input, update={"car_id":car_id, "car":car})
        
        #car.trips.append(trip)
        session.add(trip)
        session.commit()
        session.refresh(trip)
        
        return trip

    else:
        raise HTTPException(status_code=404, detail=f"No such car with id {id}")
