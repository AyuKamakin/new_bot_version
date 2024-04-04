from aiogram.fsm.state import StatesGroup, State


class Show_requests_SG(StatesGroup):
    start = State()
    show_awaiting = ()
    show_approved = ()
    show_proceeding = ()
    show_declined = ()