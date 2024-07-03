import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from googletrans import Translator
from config import TOKEN, OPENWEATHERMAP_API_KEY

import random
import keyboard as kb


bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()

@dp.message(Command('dynamic'))
async def dynamic(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Показать больше", callback_data="show_more")]
    ])
    await message.answer("Вот динамическая кнопка:", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data == "show_more")
async def show_more(callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Опция 1", callback_data="option_1")],
        [InlineKeyboardButton(text="Опция 2", callback_data="option_2")]
    ])
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)

@dp.callback_query(lambda c: c.data == "option_1")
async def option_1(callback_query: CallbackQuery):
    await callback_query.message.answer("Вы выбрали Опция 1")

@dp.callback_query(lambda c: c.data == "option_2")
async def option_2(callback_query: CallbackQuery):
    await callback_query.message.answer("Вы выбрали Опция 2")

@dp.message(Command('links'))
async def links(message: Message):
    await message.answer(f'Это кнопки с ссылками', reply_markup=kb.inline_keyboard_test)

@dp.message(F.text == "Привет")
async def left_button(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}')

@dp.message(F.text == "Пока")
async def right_button(message: Message):
   await message.answer(f'До свидания, {message.from_user.first_name}')

@dp.message(Command('voice'))
async def voice(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_voice')
    voice = FSInputFile("sample.ogg")
    await message.answer_voice(voice)

@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
    await bot.download(message.photo[-1], destination=f'img/{message.photo[-1].file_id}.jpg')

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
    await message.answer('Этот бот умеет выполнять команды: \n/start\n/help\n/weather\n/links')

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}', reply_markup=kb.main)

@dp.message(F.text)
async def translate_text(message: Message):
    translated = translator.translate(message.text, dest='en')
    await message.answer(f"Перевод: {translated.text}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

