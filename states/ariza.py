from aiogram.dispatcher.filters.state import State,StatesGroup

class Ariza(StatesGroup):
    pattern = State()
    bio = State()
    resume = State()
    tel = State()
    tg = State()
    check = State()