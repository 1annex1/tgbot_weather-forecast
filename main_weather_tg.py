import requests
import datetime
import asyncio
from config import open_weather_token, tg_bot_token  # Импорт токенов из config.py
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

# Инициализация бота и диспетчера
bot = Bot(token=tg_bot_token)
dp = Dispatcher()

# Хэндлер для команды /start
@dp.message(Command("start"))  # Используем фильтр Command для обработки команды
async def cmd_start(message: Message):
    user_first_name = message.from_user.first_name 
    await message.reply(f'Привет, {user_first_name}!Напиши город, а я скажу погоду!')

# Хэндлер для получения погоды
@dp.message()  # Обрабатываем все сообщения
async def get_weather(message: Message):
    city = message.text  # Город, который ввел пользователь
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric&lang=ru"
        )
        r.raise_for_status()  # Проверка успешности запроса
        data = r.json()

        city_name = data["name"]
        cur_weather = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"]).strftime('%H:%M:%S')

        await message.reply(
            f"Погода в городе: {city_name}\n"
            f"🌡️Температура🌡️: {cur_weather}°C\n"
            f"🌧️Влажность🌧️: {humidity}%\n"
            f"☂️Давлениe☂️: {pressure} мм.рт.ст.\n"
            f"🌪️Скорость ветра🌪️: {wind} м/с\n"
            f"☀️Восход солнца☀️: {sunrise_timestamp}\n"
            f"Хорошего дня!"
        )

    except requests.exceptions.HTTPError as http_err:
        await message.reply(f"Ошибка,проверьте название города!")
    except KeyError as key_err:
        await message.reply(f"Ошибка,проверьте название города!")
    except Exception as ex:
        await message.reply(f"Произошла ошибка: {ex}")

# Основная функция для запуска бота
async def main():
    print("Бот включен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
