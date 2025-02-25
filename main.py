import asyncio
import logging
import speedtest
import subprocess
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.utils.markdown import pre

TOKEN = "TOKEN"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Создаем клавиатуру
keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Интернет")],
    [KeyboardButton(text="Ping")],
], resize_keyboard=True)

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=keyboard)

# Обработчик кнопки "Интернет"
@dp.message(lambda message: message.text == "Интернет")
async def check_speed(message: types.Message):
    await message.answer("Пожалуйста, подождите, идет измерение скорости...")
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1_000_000  # Перевод в Мбит/с
    upload_speed = st.upload() / 1_000_000

    result = f"Скорость загрузки: {download_speed:.2f} Мбит/с\nСкорость отправки: {upload_speed:.2f} Мбит/с"
    await message.answer(pre(result), parse_mode="MarkdownV2")

# Обработчик кнопки "Ping"
@dp.message(lambda message: message.text == "Ping")
async def ask_for_ip(message: types.Message):
    await message.answer("Введите IP-адрес для проверки:")

# Обработка IP после ввода
@dp.message()
async def ping_host(message: types.Message):
    ip = message.text.strip()
    try:
        output = subprocess.run(["ping", "-c", "4", ip], capture_output=True, text=True)
        await message.answer(pre(output.stdout), parse_mode="MarkdownV2")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
