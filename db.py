from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from weather_model import WeatherData, Base
import config


DATABASE_URL = config.DATABASE_URL
async_engine = create_async_engine(DATABASE_URL)

# Async Session
async_session = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def write_current_weather(current_weather: dict):
    async with async_session() as session:
        new_weather_data = WeatherData(
            temperature=current_weather['temperature'],
            wind_speed=current_weather['wind_speed'],
            wind_direction=current_weather['wind_direction'],
            surface_pressure=current_weather['surface_pressure'],
            precipitation=current_weather['precipitation']
        )
        session.add(new_weather_data)
        await session.commit()


async def select_weather_data(limit: int = 10):
    async with async_session() as session:
        result = await session.execute(select(WeatherData).order_by(WeatherData.timestamp.desc()).limit(limit))
        return result.scalars().all()
