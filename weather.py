import aiohttp
import asyncio
import db


WEATHER_URL = 'http://api.open-meteo.com/v1/forecast'
WEATHER_UPDATE_DELAY_SECONDS = 1
SCOLTECH_LATITUDE = '55.699037'
SCOLTECH_LONGITUDE = '37.359755'


async def weather_updater():
    while True:
        asyncio.create_task(record_current_weather(SCOLTECH_LATITUDE, SCOLTECH_LONGITUDE))
        await asyncio.sleep(WEATHER_UPDATE_DELAY_SECONDS)


async def record_current_weather(latitude, longitude):
    try:
        current_weather = await fetch_weather(latitude, longitude)
        if current_weather:
            unpacked_weather = await unpacking_weather_info(current_weather)
            await db.write_current_weather(unpacked_weather)
            print('Weather is saved')
        else:
            print("No weather data available.")
    except Exception as e:
        print(f"An error occurred while recording current weather: {e}")


async def fetch_weather(latitude, longitude):
    data = {
        'latitude': latitude,
        'longitude': longitude,
        'current': 'temperature_2m,wind_speed_10m,wind_direction_10m,surface_pressure',
        'minutely_15': 'snowfall,rain,showers'
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(WEATHER_URL, data=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"HTTP Error: {response.status}")
                    return None
    except aiohttp.ClientError as e:
        print(f"HTTP Client Error: {e}")
        return None


async def unpacking_weather_info(input_weather_data):
    output_weather_data = dict()

    current = input_weather_data.get('current', {})
    output_weather_data['temperature'] = current.get('temperature_2m', "N/A")
    output_weather_data['wind_speed'] = current.get('wind_speed_10m', "N/A")
    output_weather_data['surface_pressure'] = current.get('surface_pressure', "N/A")

    wind_degree = current.get('wind_direction_10m')
    if wind_degree is not None:
        output_weather_data['wind_direction'] = await get_wind_direction(wind_degree)
    else:
        output_weather_data['wind_direction'] = "N/A"

    precipitation = await precipitation_unpacking(input_weather_data)
    output_weather_data['precipitation'] = precipitation if precipitation else "N/A"

    return output_weather_data


async def precipitation_unpacking(input_weather_data):
    precipitation = dict()

    precipitation['snowfall'] = round(sum(input_weather_data['minutely_15']['snowfall']), -2)
    precipitation['rain'] = round(sum(input_weather_data['minutely_15']['rain']), -2)
    precipitation['showers'] = round(sum(input_weather_data['minutely_15']['showers']), -2)

    return precipitation


async def get_wind_direction(wind_degree):
    wind_degree = wind_degree % 360

    if 0 <= wind_degree < 22.5 or 337.5 <= wind_degree < 360:
        return 'С'
    elif 22.5 <= wind_degree < 67.5:
        return 'СВ'
    elif 67.5 <= wind_degree < 112.5:
        return 'В'
    elif 112.5 <= wind_degree < 157.5:
        return 'ЮВ'
    elif 157.5 <= wind_degree < 202.5:
        return 'Ю'
    elif 202.5 <= wind_degree < 247.5:
        return 'ЮЗ'
    elif 247.5 <= wind_degree < 292.5:
        return 'З'
    elif 292.5 <= wind_degree < 337.5:
        return 'СЗ'
