from aiogram.fsm.state import StatesGroup, State


class Start_SG(StatesGroup):
    start = State()
    menu = State()