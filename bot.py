import requests as req
import datetime
from config import TG_BOT_TOKEN, TOKEN
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=TG_BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply('Привет! Хочешь узнать погоду? Тогда напиши название города!')

@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        'Clear': 'Ясно \U0001F324',
        'Clouds': 'Облачно \U00002601',
        'Mist': 'Туман \U0001F32B',
        'Fog': 'Туман \U0001F32B',
        'Snow': 'Снег \U00002744',
        'Rain': 'Дождь \U0001F327',
        'Drizzle': 'Мелкий дождь \U0001F327',
        'Thunderstorm': 'Гроза \U0001F329',
    }

    try:
        r = req.get(f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={TOKEN}&units=metric')
        data = r.json()

        city = data['name']
        current_temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        current_humidity = data['main']['humidity']
        current_pressure = data['main']['pressure']
        wind_speed = data['wind']['speed']
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        daylight_hours = sunset - sunrise

        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'Не могу понять, что за погода, придется смотреть самому!'

        await message.reply(f'{datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}\n'
              f'Погода в городе {city}\n'
              f'Температура: {current_temp} °C {wd}\n'
              f'Ощущается как: {feels_like} °C\n'
              f'Влажность: {current_humidity}%\n'
              f'Давление: {current_pressure} мм.рт.ст\n'
              f'Скорость ветра: {wind_speed} м/с\n'
              f'Время рассвета: {sunrise}\n'
              f'Время заката: {sunset}\n'
              f'Продолжительность светового дня: {daylight_hours}')

    except Exception as e:
        print(e)
        await message.reply("\U00002620 Проверьте название города \U00002620")

if __name__ == '__main__':
    executor.start_polling(dp)