import os
from datetime import datetime
from fastapi import FastAPI, HTTPException
from starlette.config import Config
from pydantic import BaseModel, Field
import databases
import sqlalchemy
from typing import Optional


config = Config(".env")

DATABASE_URL = config("DATABASE_URL", cast=str)

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

solar_array_telemetry = sqlalchemy.Table(
    "solar_array_telemetry",
    metadata,
    sqlalchemy.Column("timestamp", sqlalchemy.DateTime),
    sqlalchemy.Column("active_energy_delivered_received", sqlalchemy.Float),
    sqlalchemy.Column("current_phase_average", sqlalchemy.Float),
    sqlalchemy.Column("active_power", sqlalchemy.Float),
    sqlalchemy.Column("performance_ratio", sqlalchemy.Float),
    sqlalchemy.Column("wind_speed", sqlalchemy.Float),
    sqlalchemy.Column("weather_temperature_celsius", sqlalchemy.Float),
    sqlalchemy.Column("weather_relative_humidity", sqlalchemy.Float),
    sqlalchemy.Column("global_horizontal_radiation", sqlalchemy.Float),
    sqlalchemy.Column("diffuse_horizontal_radiation", sqlalchemy.Float),
    sqlalchemy.Column("wind_direction", sqlalchemy.Float),
    sqlalchemy.Column("weather_daily_rainfall", sqlalchemy.Float),
    sqlalchemy.Column("radiation_global_tilted", sqlalchemy.Float),
    sqlalchemy.Column("radiation_diffuse_tilted", sqlalchemy.Float),
)

app = FastAPI()

class Telemetry(BaseModel):
    timestamp: datetime
    active_energy_delivered_received: float = Field(..., alias="Active_Energy_Delivered_Received")
    current_phase_average: float = Field(..., alias="Current_Phase_Average")
    active_power: float = Field(..., alias="Active_Power")
    performance_ratio: Optional[float] = Field(None, alias="Performance_Ratio")
    wind_speed: Optional[float] = Field(None, alias="Wind_Speed")
    weather_temperature_celsius: float = Field(..., alias="Weather_Temperature_Celsius")
    weather_relative_humidity: float = Field(..., alias="Weather_Relative_Humidity")
    global_horizontal_radiation: float = Field(..., alias="Global_Horizontal_Radiation")
    diffuse_horizontal_radiation: float = Field(..., alias="Diffuse_Horizontal_Radiation")
    wind_direction: float = Field(..., alias="Wind_Direction")
    weather_daily_rainfall: float = Field(..., alias="Weather_Daily_Rainfall")
    radiation_global_tilted: Optional[float] = Field(None, alias="Radiation_Global_Tilted")
    radiation_diffuse_tilted: Optional[float] = Field(None, alias="Radiation_Diffuse_Tilted")

    class Config:
        allow_population_by_field_name = True # # enable using "alias" in the fields for serialization and deserialization

@app.on_event("startup") # handle connecting to the db when the app starts
async def startup():
    await database.connect()

@app.on_event("shutdown") # handle disconnecting from the db when the app shuts down
async def shutdown():
    await database.disconnect()

@app.get("/telemetry/latest", response_model=Telemetry)
async def get_latest_telemetry():
    query = solar_array_telemetry.select().order_by(sqlalchemy.desc(solar_array_telemetry.c.timestamp)).limit(1)
    result = await database.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail="No telemetry data found")
    return result
