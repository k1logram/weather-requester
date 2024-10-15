import asyncio
import db
import weather


async def main():
    await db.create_tables()
    asyncio.run(await weather.weather_updater())


if __name__ == '__main__':
    asyncio.run(main())
