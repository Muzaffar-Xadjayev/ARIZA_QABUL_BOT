from aiogram.dispatcher.filters.state import State, StatesGroup

class Advers(StatesGroup):
    text = State()

class Delete(StatesGroup):
    msg = State()

class Create(StatesGroup):
    title=State()
    question=State()

class One(StatesGroup):
    id = State()
    text = State()

class Add_Question(StatesGroup):
    title = State()
    text = State()

class Remove_Question(StatesGroup):
    title = State()