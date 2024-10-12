import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

import python_weather

TOKEN = ""

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Введите город, погоду которого вы хотите узнать")

@dp.message()
async def echo_handler(message: Message) -> None:
    if message.text.startswith('/'):
        return
    async with python_weather.Client(unit=python_weather.METRIC) as client:
        city =  message.text
        try:
            weather = await client.get(city)
        except:
            await message.answer("Такой город не найден")
        finally:
            await message.answer(f"Погода в городе \"{city}\":\nТемпература {weather.temperature}°C\nСкорость ветра {weather.wind_speed} м\\с\nВлажность {weather.humidity}%\n")

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
