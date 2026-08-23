from aiogram.fsm.state import State, StatesGroup

class CategoryStates(StatesGroup):
    waiting_for_category = State()

class AddStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_price = State()
    waiting_for_category = State()