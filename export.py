import asyncio
import openpyxl
import db

TABLE_HEADERS = ['Температура', 'Скорость ветра', 'Направление ветра', 'Атмосферное давление', 'Осадки', 'Дата']
EXPORT_FILENAME = 'weather_data.xlsx'


async def export_to_excel():
    weather_data = await db.select_weather_data()
    records_count_total = len(weather_data)
    if records_count_total == 0:
        print('Weather data is empty')
        return

    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    worksheet.append(TABLE_HEADERS)

    append_weather_data(worksheet, weather_data)

    workbook.save(EXPORT_FILENAME)
    print('Data export completed successfully')
    print('Total records -', records_count_total)


def append_weather_data(worksheet, weather_data):
    for weather_row in weather_data:
        precipitation = unpacking_precipitation(weather_row.precipitation)
        worksheet.append([
            weather_row.temperature,
            weather_row.wind_speed,
            weather_row.wind_direction,
            weather_row.surface_pressure,
            precipitation,
            weather_row.timestamp,
        ])


def unpacking_precipitation(input_precipitation):
    output_precipitation = f'''Дождь - {input_precipitation["rain"]}
Ливень - {input_precipitation["showers"]}
Снег - {input_precipitation["snowfall"]}'''

    return output_precipitation


if __name__ == '__main__':
    asyncio.run(export_to_excel())
