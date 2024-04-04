from aiogram.fsm.state import StatesGroup, State


class Change_User_SG(StatesGroup):
    start = State()
    enter_login = State()