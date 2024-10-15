from sqlalchemy import Column, Integer, Float, String, DateTime, func, JSON
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class WeatherData(Base):
    __tablename__ = 'weather_data'
    id = Column(Integer, primary_key=True)
    temperature = Column(Float)
    wind_speed = Column(Float)
    wind_direction = Column(String)
    surface_pressure = Column(Float)
    precipitation = Column(JSON)
    timestamp = Column(DateTime, default=func.now())




