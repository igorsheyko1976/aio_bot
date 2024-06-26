import asyncio
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from config import TOKEN, OPENWEATHERMAP_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Novorossiysk&appid={OPENWEATHERMAP_API_KEY}&units=metric&lang=ru"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data

@dp.message(Command('weather'))
async def weather(message: Message):
    weather_data = await get_weather()
    if weather_data:
        description = weather_data['weather'][0]['description']
        temp = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']

        weather_report = (
            f"Погода в Новороссийске на сегодня:\n"
            f"Описание: {description.capitalize()}\n"
            f"Температура: {temp}°C\n"
            f"Ощущается как: {feels_like}°C\n"
            f"Влажность: {humidity}%\n"
            f"Скорость ветра: {wind_speed} м/с"
        )
    else:
        weather_report = "Не удалось получить данные о погоде."

    await message.answer(weather_report)

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет выполнять команды: \n/start\n/help\n/weather')

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет, я бот, который показывает погоду в Новороссийске!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())