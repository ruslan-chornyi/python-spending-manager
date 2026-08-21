import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from storage import load_expense

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Hello! I'm your expense bot.")

@dp.message(Command("all"))
async def all_handler(message: types.Message):
    expenses = load_expense()

    lines = [str(e) for e in expenses]
    text = "\n".join(lines)
    await message.answer(text)

@dp.message(Command("total"))
async def total_handler(message: types.Message):
    expenses = load_expense()
    total = 0
    for p in expenses:
        total += p.price
    await message.answer(f"Total amount = {total}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())