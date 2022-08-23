from fastapi import FastAPI, HTTPException, Depends
import uvicorn
from schemas import CarOutput, TripInput, TripOutput, CarInput, Car, Trip
from sqlmodel import create_engine, Session, SQLModel, select


app = FastAPI()

engine = create_engine(
    "sqlite:///carsharing.db",
    connect_args= {"check_same_thread":False},
    echo= True
)
def get_session():
    with Session(engine) as session:
        yield session

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.get("/api/cars")
def get_cars(size: str|None = None, doors: int|None = None, session: Session = Depends(get_session)) -> list:
    
    query = select(Car)
    if size:
        query = query.where(Car.size == size)
    if doors:
        query = query.where(Car.doors >= doors)

    result = session.exec(query).all()
    return result 

@app.get("/api/cars/{id}", response_model=CarOutput)
def get_cars_id(id:int, session: Session = Depends(get_session)) -> dict:
    car = session.get(Car, id)
    if car:
        return car
    else:
        raise HTTPException(status_code=404, detail=f"No such car with id {id}")
    
@app.post("/api/cars", response_model=Car)
def add_car(car_input: CarInput, session: Session = Depends(get_session)) -> CarOutput:
     
    new_car = Car.from_orm(car_input)
    session.add(new_car)
    session.commit()
    session.refresh(new_car)
    return new_car


@app.delete("/api/cars/{id}", status_code= 200)
def remove_car(id: int, session: Session = Depends(get_session)):
    car = session.get(Car, id)
    if car:
        session.delete(car)
        session.commit()

    else:
        raise HTTPException(status_code=404, detail=f"No such car with id {id}")


@app.put("/api/cars/{id}", response_model=CarOutput)
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

@app.post("/api/cars/{id}/trips", response_model=TripInput)
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

    
        

if __name__ == '__main__':
    uvicorn.run("carsharing:app", reload=True)