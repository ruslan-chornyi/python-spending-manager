import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from storage import load_expense
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage


class CategoryStates(StatesGroup):
    waiting_for_category = State()


load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(Command("category"))
async def category_handler(message: types.Message, state: FSMContext):
    expenses = load_expense()
    categories = {e.category for e in expenses}

    if not categories:
        await message.answer("No expenses yet")
        return

    await message.answer(f"Available categories: {', '.join(categories)}\nWhich one?")
    await state.set_state(CategoryStates.waiting_for_category)

@dp.message(CategoryStates.waiting_for_category)
async def category_response_handler(message: types.Message, state: FSMContext):
    if message.text.startswith("/"):
        await state.clear()
        await message.answer("Cancelled category selection.")
        return

    usr_category = message.text.lower()
    expenses = load_expense()

    total = 0
    lines = []
    for c in expenses:
        if c.category == usr_category:
            lines.append(str(c))
            total += c.price

    text = "\n".join(lines) if lines else "No expenses in this category"
    await message.answer(f"{text}\nTotal: {total}$")

    await state.clear()

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

    for e in expenses:
        total += e.price
    await message.answer(f"Total amount = {total}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())