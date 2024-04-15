from aiogram.fsm.state import StatesGroup, State


class Show_requests_SG(StatesGroup):
    start = State()
    show_awaiting = State()
    show_approved = State()
    show_proceeding = State()
    show_declined = State()
    show_ready_return = State()
    show_proceeding_return = State()
    show_return_done = State()
    show_in_usage = State()
    show_chosen_request = State()
    show_or_delete_chosen_request = State()
    confirm_deletion = State()
    deletion_confirmed = State()
