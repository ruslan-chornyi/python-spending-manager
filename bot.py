import asyncio, os, uuid
from storage import load_expense_by_user, save_expense, delete_expense
from models import Expense
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from states import CategoryStates, AddStates, DeleteStates

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

#async command start
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("""Hello! I'm your expense bot.
You can use these commands: 
/add - add a new expense to your list
/all - show all expenses
/total - show total sum of all expenses
/category - show expense by 1 category
/delete - deleting an expense
""")

#async command add
@dp.message(Command("add"))
async def add_handler(message: types.Message, state: FSMContext):
    await message.answer("What did you spend on?")
    await state.set_state(AddStates.waiting_for_name)

@dp.message(AddStates.waiting_for_name)
async def add_name_handler(message: types.Message, state: FSMContext):
    if message.text.startswith("/"):
        await state.clear()
        await message.answer("Cancelled adding expense.")
        return

    await state.update_data(name=message.text)
    await message.answer("How much did it cost?")
    await state.set_state(AddStates.waiting_for_price)

@dp.message(AddStates.waiting_for_price)
async def add_price_handler(message: types.Message, state: FSMContext):
    if message.text.startswith("/"):
        await state.clear()
        await message.answer("Cancelled adding expense.")
        return

    try:
        price = int(message.text)
    except ValueError:
        await message.answer("Please enter a valid number.")
        return

    await state.update_data(price=price)
    await message.answer("Which category?")
    await state.set_state(AddStates.waiting_for_category)

@dp.message(AddStates.waiting_for_category)
async def add_category_handler(message: types.Message, state: FSMContext):
    if message.text.startswith("/"):
        await state.clear()
        await message.answer("Cancelled adding expense.")
        return

    category = message.text.lower()
    data = await state.get_data()
    expense_id = str(uuid.uuid4())

    expense = Expense(expense_id ,message.from_user.id, data["name"], data["price"], category)
    save_expense(expense)

    await message.answer(f"Added: {expense}")
    await state.clear()

#async command all
@dp.message(Command("all"))
async def all_handler(message: types.Message):
    expenses = load_expense_by_user(message.from_user.id)

    lines = [str(e) for e in expenses]
    text = "".join(lines)
    await message.answer(text)

#async command total
@dp.message(Command("total"))
async def total_handler(message: types.Message):
    expenses = load_expense_by_user(message.from_user.id)
    total = 0

    for e in expenses:
        total += e.price
    await message.answer(f"Total amount = {total}")

#async command category
@dp.message(Command("category"))
async def category_handler(message: types.Message, state: FSMContext):
    expenses = load_expense_by_user(message.from_user.id)
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
    expenses = load_expense_by_user(message.from_user.id)

    total = 0
    lines = []
    for c in expenses:
        if c.category == usr_category:
            lines.append(str(c))
            total += c.price

    text = "\n".join(lines) if lines else "No expenses in this category"
    await message.answer(f"{text}\nTotal: {total}$")

    await state.clear()

#delete function
@dp.message(Command("delete"))
async def delete_handler(message: types.Message, state: FSMContext):
    expenses = load_expense_by_user(message.from_user.id)

    if not expenses:
        await message.answer("No expenses to delete")
        return

    ex_id = []
    lines = []
    for i, e in enumerate(expenses, start=1):
        ex_id.append(e.expense_id)
        lines.append(f"{i} - {e}")

    text = "".join(lines)
    await message.answer(f"{text}\nWhich number do you want to delete?")

    await state.update_data(ex_id=ex_id)
    await state.set_state(DeleteStates.waiting_for_number)

@dp.message(DeleteStates.waiting_for_number)
async def delete_number_handler(message: types.Message, state: FSMContext):
    if message.text.startswith("/"):
        await state.clear()
        await message.answer("Cancelled deletion.")
        return

    if not message.text.isdigit():
        await message.answer("Please enter a valid number.")
        return

    user_delete_num = int(message.text)
    data = await state.get_data()
    ex_id = data["ex_id"]

    if user_delete_num < 1 or user_delete_num > len(ex_id):
        await message.answer("Number out of range.")
        return

    selected_id = ex_id[user_delete_num - 1]

    if delete_expense(selected_id):
        await message.answer("Deleted successfully!")
    else:
        await message.answer("Expense not found.")

    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())