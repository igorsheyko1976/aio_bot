import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

from config import TOKEN, THE_DOG_API_KEY


bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_dog_image():
    url = "https://api.thedogapi.com/v1/images/search"
    headers = {"x-api-key": THE_DOG_API_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data[0]['url']

@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Я могу прислать картинку с милыми животными. Используй команду /dog.")

@dp.message(Command("dog"))
async def dog_command(message: Message):
    dog_image_url = get_dog_image()
    await message.answer_photo(photo=dog_image_url)

async def main():
   await dp.start_polling(bot)

if __name__ == '__main__':
   asyncio.run(main())