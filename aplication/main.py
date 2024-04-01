import models
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from pydantic import BaseModel
from models import Record, Continuous, Tuning, Schedule
from sqlalchemy.sql.expression import func
import requests

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")


class RecordRequest(BaseModel):
    time_start: str
    time_end: str
    temperature: str
    humidity: str


class ScheduleRequest(BaseModel):
    turned_on: bool


class ContinuousRequest(BaseModel):
    temperature: str
    humidity: str
    turned_on: bool


class ContinuousStartRequest(BaseModel):
    turned_on: bool


class TuningTempRequest(BaseModel):
    turned_on_temp: bool


class TuningHumRequest(BaseModel):
    turned_on_hum: bool


class DeleteRequest(BaseModel):
    id: str


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def dashboard(request: Request, db: Session = Depends(get_db)):
    # startowe 'ładowanie' z bazy danych
    records = db.query(Record).order_by(func.length(Record.time_start), Record.time_start)
    schedule = db.query(Schedule)
    continous = db.query(Continuous)
    tuning = db.query(Tuning)
    # startowe pobranie informacji o pogodzie
    # Klucz API z OpenWeatherMap
    api_key = "d6c456f929e533004247557e7f0a53c1"
    # Pobierz dane o pogodzie dla określonego miasta
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Warsaw&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    # Przetwarzanie danych o pogodzie
    weather_description = data["weather"][0]["description"]
    temperature = round(data["main"]["temp"] - 273.15, 2)
    humidity = data["main"]["humidity"]

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "records": records,
        "schedule": schedule,
        "continous": continous,
        "tuning": tuning,
        "weather_description": weather_description,
        "temperature": temperature,
        "humidity": humidity
    })


@app.post("/records")
def create_record(record_request: RecordRequest, db: Session = Depends(get_db)):
    # tworzy wpis do harmonogramu w bazie danych
    record = Record()
    record.time_start = record_request.time_start
    record.time_end = record_request.time_end
    record.temperature = record_request.temperature
    record.humidity = record_request.humidity
    db.add(record)
    db.commit()
    return {
        "code": "success",
        "message": "record created"
    }


@app.delete("/records/delete")
def delete_record(delete_request: DeleteRequest, db: Session = Depends(get_db)):
    # usuwa wpis w harmonogramie w bazie danych
    record = Record()
    record.id = delete_request.id
    to_delete_record = db.query(Record).filter(Record.id == record.id).first()
    if to_delete_record is None:
        return {
            "code": "NOT success",
            "message": "record NOT deleted, NOT found"
        }
    db.delete(to_delete_record)
    db.commit()
    return {
        "code": "success",
        "message": "record deleted"
    }


@app.patch("/schedule")
def update_schedule(schedule_request: ScheduleRequest, db: Session = Depends(get_db)):
    # ustawia start pracy harmonogramu bazie danych
    schedule = Schedule()
    schedule.turned_on = schedule_request.turned_on
    old_schedule = db.query(Schedule)
    old_schedule.update({'turned_on': schedule.turned_on})
    db.commit()
    return {
        "code": "success",
        "message": "schedule started"
    }


@app.patch("/continuous")
def update_continuous(continuous_request: ContinuousRequest, db: Session = Depends(get_db)):
    # ustawia wartosci i start trybu ciaglego w bazie danych
    cont = Continuous()
    cont.temperature = continuous_request.temperature
    cont.humidity = continuous_request.humidity
    cont.turned_on = continuous_request.turned_on
    old_continuous = db.query(Continuous)
    old_continuous.update({
        'temperature': cont.temperature,
        'humidity': cont.humidity,
        'turned_on': cont.turned_on})
    db.commit()
    return {
        "code": "success",
        "message": "continuous updated and started"
    }


@app.patch("/continuous/run")
def update_continuous_run(continuous_start_request: ContinuousStartRequest, db: Session = Depends(get_db)):
    # ustawia start/koniec pracy ciągłego trybu bazie danych
    cont = Continuous()
    cont.turned_on = continuous_start_request.turned_on
    old_continuous = db.query(Continuous)
    old_continuous.update({'turned_on': cont.turned_on})
    db.commit()
    return {
        "code": "success",
        "message": "continuous start updated"
    }


@app.patch("/tuning/temperature")
def update_tuning_temp(tuning_request: TuningTempRequest, db: Session = Depends(get_db)):
    # ustawia start tuningu odpowiedniego regulatora w bazie danych
    tuning = Tuning()
    tuning.turned_on_temp = tuning_request.turned_on_temp
    old_tuning = db.query(Tuning)
    old_tuning.update(
        {'turned_on_temp': tuning.turned_on_temp})
    db.commit()
    return {
        "code": "success",
        "message": "tuning temperature started"
    }


@app.patch("/tuning/humidity")
def update_tuning_hum(tuning_request: TuningHumRequest, db: Session = Depends(get_db)):
    # ustawia start tuningu odpowiedniego regulatora w bazie danych
    tuning = Tuning()
    tuning.turned_on_hum = tuning_request.turned_on_hum
    old_tuning = db.query(Tuning)
    old_tuning.update(
        {'turned_on_hum': tuning.turned_on_hum})
    db.commit()
    return {
        "code": "success",
        "message": "tuning humidity started"
    }



