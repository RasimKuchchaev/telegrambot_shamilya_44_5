
import logging
import os
import asyncio
from aiogram import Bot, Dispatcher, types, Router 
from aiogram.types import ContentType, FSInputFile 
from aiogram.filters import Command
from PIL import Image, ImageDraw, ImageFont

with open("conf.txt") as file:
    token = file.read()
    
# Установите ваш токен бота
TOKEN = token

# Создаем бота и диспетчер
bot = Bot (token=TOKEN) 
dp = Dispatcher()
router = Router()

#Логирование
logging.basicConfig(level=logging.INFO)
# Словарь для хранения изображений пользователей 
user_data = {}

# Обработчик команды /start
@router.message(Command("start"))
async def send_welcome(message: types. Message):
    await message.answer("Привет! Отправь мне картинку, и я помогу сделать мем.")


async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True) 
    await dp.start_polling(bot)
    await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())